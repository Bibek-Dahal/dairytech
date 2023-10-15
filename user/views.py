from typing import Any
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView,TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import BadRequest
from dairyapp.models import Dairy, FatRate, MilkRecord

from django.db.models import Q
from django.db.models import Avg,Sum
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.generic import View
from django.views.generic.edit import CreateView,UpdateView
from user.forms import UserProfileForm, UserUpdateForm
from user.models import Profile
from django.contrib import messages

from utils.dairyapp.commonutils import convert_nepali_date, getFatBasedOnDate, is_valid_date



# Create your views here.

@method_decorator(login_required(login_url='account_login'),name="dispatch")
class HomeView(ListView):
    model = Dairy
    template_name = 'user/index.html'
    context_object_name = 'dairies'

    def get_queryset(self):
        qs = super().get_queryset().filter(members__in=[self.request.user])
        print('qs',qs)
        return qs
    # def get(self,request):
    #     dairies = Dairy.objects.filter(members__in=[request.user])
    #     print('dairies',dairies)

    #     return render(request,'user/index.html')


@method_decorator(login_required(login_url='account_login'),name="dispatch")
class MemberMilkRecord(ListView):
    model = MilkRecord
    context_object_name = "milkrecords"
    template_name = "user/member_milkrecord_list_copy.html"
    paginate_by = 16

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['dairy'] = self.kwargs['dairy']
        # context['id'] = self.kwargs['id']
        context['start_date'] = is_valid_date(self.request.GET.get('start_date',""))
        context['end_date'] = is_valid_date(self.request.GET.get('end_date',""))
        context['shift'] = self.request.GET.get('shift')
        context['date'] = is_valid_date(self.request.GET.get('date',""))
        context['count'] = self.kwargs['count']
        context['total_milk_wieght'] = self.kwargs['total_milk_wieght']
        context['avg_fat'] = round(self.kwargs['avg_fat'],3)
        context['total_price'] = self.kwargs['total_price']
        context['fat_rate'] = self.kwargs['fat_rate']
        context['bonous'] = self.kwargs['bonous']
        context['total_fat_rate'] = self.kwargs['total_fat_rate']
        dairy = get_object_or_404(Dairy,name=self.kwargs['dairy'])
        context['members'] = dairy.members.all()
        

        
        return context
    
        
    
    
    
    def get_queryset(self):
        try:
            request = self.request
            print("date",self.request.GET.get('date'))
            print("name",self.request.GET.get('name'))
            shift = request.GET.get('shift')
            date = convert_nepali_date(request.GET.get('date',''))
            start_date = convert_nepali_date(request.GET.get('start_date',''))
            print("start_date",start_date)
            end_date = convert_nepali_date(request.GET.get('end_date',''))
            print("end_date",end_date)
            
            # return super().get_queryset() 
            user = self.request.user
            dairy = get_object_or_404(Dairy,name=self.kwargs['dairy'])
            queryset  = super().get_queryset() 
            filters = Q(dairy=dairy,user=user)
            # return MilkRecord.objects.filter(dairy=dairy,dairy__user=self.request.user,user=user)
        
            if shift:
                print("inside shift--------------")
                print("shift",shift)
                filters &= Q(shift=shift)

            if date:
                filters &= Q(date=date)

            if start_date and end_date:
                queryset = queryset.filter(date__gte=start_date, date__lte=end_date)
            elif start_date:
                filters &= Q(date__gte=start_date)
            elif end_date:
                filters &= Q(date__lte=end_date)
                
                

            # if start_date and end_date:
            #      filters &= Q(date>=start_date and date<=end_date)
            


            def seedMilkRecord():
                print("inside milk record")
                import random
                i = 1
                for i in range(10,30):
                    date = f"2023-09-{i}"
                    if i<9:
                        date = f"2023-07-0{i}"
                    MilkRecord.objects.create(
                        dairy = dairy,
                        user = user,
                        shift = "night",
                        milk_weight = random.randint(1,20),
                        milk_fat = random.randint(1,6),
                        date = date
                    )
            # seedMilkRecord()
            qs = queryset.filter(filters)
            count = qs.count()
            print("count",count)
            self.kwargs['count'] = count
            self.kwargs['total_milk_wieght'] = 0
            self.kwargs['avg_fat'] = 0
            self.kwargs['total_price'] = 0
            self.kwargs['fat_rate'] = None
            self.kwargs['bonous'] = 0
            self.kwargs['total_fat_rate'] = 0

            fat_rate = None
            total_price = 0

            if shift and start_date and end_date:
                print("inside first if")
                if qs:
                    print("inside secode if")
                    # print("+++++++++++",getFatBasedOnDate(start_date,end_date))
                    """
                    perform qs operation if only qs is not empty
                    """
                
                    milk_wg = qs.aggregate(Sum("milk_weight")).get('milk_weight__sum')
                    avg_fat = qs.aggregate(Avg("milk_fat")).get('milk_fat__avg')
                    self.kwargs['total_milk_wieght'] = milk_wg
                    self.kwargs['avg_fat'] = avg_fat
                    print("milk_weight",milk_wg)
                    print("average_fat",avg_fat)


                    #filter the fat rate within date range
                    fat_rate_obj = FatRate.objects.filter(dairy=dairy,created_at__date__lte=end_date,created_at__date__gte=start_date)

                    print("count obj---",fat_rate_obj.count())

                    if fat_rate_obj.count()>1:
                        #raise error if multiple fat range exists within date range
                        messages.error(request,message= _("Cannot apply filter witin date range. Multiple fat rate exists."))

                    # elif getFatBasedOnDate(start_date,end_date):
                    #     print("inside first elif")
                    #     fat_rate_obj = getFatBasedOnDate(start_date,end_date)
                    #     fat_rate = fat_rate_obj.get_fat_rate
                    #     self.kwargs['fat_rate'] = fat_rate_obj.fat_rate
                    #     self.kwargs['bonous'] = fat_rate_obj.bonous_amount
                    #     self.kwargs['total_fat_rate'] = fat_rate
                        
                        # print('fat rate obj count',fat_rate_obj.count())
                    
                        
                        # return redirect("dairyapp:member_milk_record",id=user.id,dairy=dairy.name)
                    elif fat_rate_obj.count() == 0:
                        print('inisde second elif')
                        #calculate fat rates if provided date range is before fat rate creation date
                        
                        ft = FatRate.objects.filter(dairy=dairy).first()
                        
                        if ft:
                            fat_rate_obj = ft
                            fat_rate = fat_rate_obj.get_fat_rate
                            self.kwargs['fat_rate'] = fat_rate_obj.fat_rate
                            self.kwargs['bonous'] = fat_rate_obj.bonous_amount
                            self.kwargs['total_fat_rate'] = fat_rate
                            print("fat rate===",fat_rate)
                        else:
                        
                            messages.error(request, _("Fat rate with in specified date range is not defined."))
                    
                        # return redirect("dairyapp:member_milk_record",id=user.id,dairy=dairy.name)
                    else:
                        fat_rate = fat_rate_obj.first().get_fat_rate
                        self.kwargs['fat_rate'] = fat_rate_obj.first().fat_rate
                        self.kwargs['bonous'] = fat_rate_obj.first().bonous_amount
                        self.kwargs['total_fat_rate'] = fat_rate
                        print("fat rate===",fat_rate)
                    
                    try:
                        total_price = fat_rate*milk_wg*avg_fat
                    except Exception as e:
                        total_price = 0
                    self.kwargs['total_price'] = total_price

                    print("total price===",total_price)
                    # print("total price==",total_price)
                    pass


                
            return queryset.filter(filters)
        except Exception as e:
            print(e)
            raise BadRequest("Bad Request")


             
       

class UpdateProfileView(View):
    template_name = 'user/profile/profile.html'

    form_class = UserProfileForm

    def get(self,request):
        form = UserProfileForm()
        return render(request,self.template_name,{'form':form})
    
    def post(self,request):
        form = UserProfileForm(self.request.POST,files=request.FILES)
        files = request.FILES
        print("files",files)
        if form.is_valid():
            profile = Profile.objects.get(user=request.user)
            profile.profile_pic = files.get('profile_pic')
            profile.save()
            return redirect("user:profile")
        return render(request,self.template_name,{'form':form})
    
class UpdateUserView(View):
    template_name = 'user/update_user.html'
    form_class = UserUpdateForm
    def get(self,request):
        form = self.form_class(instance=self.request.user)
        return render(request,self.template_name,{'form':form})
    
    def post(self,request):
        form = self.form_class(request.POST,instance=self.request.user)

        if form.is_valid():
            form.save()
            messages.success(request,_("User updated successfully"))
            return redirect('dairyapp:homepage')
        return render(request,self.template_name,{'form':form})

    
    

    
    