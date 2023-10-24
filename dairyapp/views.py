import io
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.http import Http404, HttpResponse, HttpResponseRedirect,HttpResponseForbidden,HttpResponseNotFound
from dairyapp.mixins import PaginationMixin 
from dairyapp.models import *
from .forms import *
from django.views.generic import ListView,DetailView
from django.views.generic.edit import UpdateView,DeleteView,CreateView
from django.shortcuts import get_object_or_404
from django.contrib import messages
# Create your views here.
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Avg,Sum
from .decorators import verified_dairy_user
import uuid
import requests as req
from django.views.generic import View
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from weasyprint import HTML
from utils.dairyapp.commonutils import convert_nepali_date, get_fat_rate_fun, getFatBasedOnDate, is_valid_date, sendMial
from django.conf import settings
from django.forms import formset_factory,modelformset_factory
from django.core.exceptions import BadRequest
import json
import requests
from .tasks import sendMial as sm
from django.core.exceptions import PermissionDenied



@method_decorator(login_required(login_url='account_login'),name="dispatch")
# @method_decorator(verified_dairy_user,name="dispatch")
class HomeView(View):
    def get(self,request):
        auser = get_user_model()
        print("user model",auser)
        user = self.request.user
        print("inside home view")
        print(user)
        dairies = Dairy.objects.filter(user = user)
        print(dairies)
        

        if Dairy.objects.filter(user = user):
            fat_rates = FatRate.objects.filter(dairy__in = dairies)
            print(fat_rates)
            # dairy = Dairy.objects.get(name = self.request.GET.get('dairy'))
            # milk_records = MilkRecord.objects.filter(dairy=dairy,user=user)

            print("======")
            print("dairies",dairies)

            context = {
                'dairies':dairies,
                'name':'Dashboard'
                # "milk_records":milk_records,
                # 'fat_rates':fat_rates
            }
            return render(request,"dairyapp/index.html",context)

        else:
            # pass

            dairies_list = Dairy.objects.filter()
            return render(request,"dairyapp/index.html")

@method_decorator(login_required(login_url='account_login'),name="dispatch")
@method_decorator(verified_dairy_user,name="dispatch")
class FatListView(ListView):
    model = FatRate
    paginate_by = 100
    template_name = "fatrate_list"
    context_object_name = "fatrates"

    def get_context_data(self, **kwargs) :
        context =  super().get_context_data(**kwargs)
        context['name'] = 'Fat Rates'
        return context

    def get_queryset(self):
        qs = super().get_queryset().filter(dairy__user = self.request.user)
        print(qs)
        return qs
    
class EditFatView(UpdateView):
    pass

@method_decorator(login_required(login_url='account_login'),name="dispatch")
@method_decorator(verified_dairy_user,name="dispatch")
class CreateFatView(View):
    def get(self,request,*args,**kwargs):
        print(self.request.user)
        dairies = Dairy.objects.filter(user=self.request.user)
        print(dairies)
        form = CreateFatForm(self.request,initial={'fat_rate':20})
        print(form.fields['dairy'])
        
        return render(request,"dairyapp/create_fat.html",{'form':form})

    def post(self,request,*args,**kwargs):
        form = CreateFatForm(self.request,request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,_("Fat Rate Created Successfully."))
            return HttpResponseRedirect(reverse("dairyapp:fat_list"))
        return render(request,"dairyapp/create_fat.html",{'form':form})


@method_decorator(login_required(login_url='account_login'),name="dispatch")
@method_decorator(verified_dairy_user,name="dispatch")
class UpdateFatView(View):
    def get(self,request,*args,**kwargs):

            fatrate =get_object_or_404(FatRate,id=self.kwargs['id'],dairy__user=self.request.user)
            # fatrate = FatRate.objects.get(id=self.kwargs['id'])
            # if fatrate and fatrate.dairy.user == request.user:
                # dairy = Dairy.objects.get()
            form = CreateFatForm(self.request,instance=fatrate)
            
            return render(request,'dairyapp/edit_fat.html',{'form':form})
            # else:
            #     # return HttpResponse("404")
        
        
    def post(self,request,*args,**kwargs):
            print("inside post")
            fatrate = get_object_or_404(FatRate,id=self.kwargs['id'],dairy__user=self.request.user)
            # FatRate.objects.get(id=self.kwargs['id'])
            # if fatrate and fatrate.dairy.user == request.user:
            print("inside if")
            # dairy = Dairy.objects.get()
            form = CreateFatForm(self.request,request.POST,instance=fatrate)
            if form.is_valid():
                print("inside valid data")
                form.save()
                return HttpResponseRedirect(reverse("dairyapp:fat_list"))
            print("inside else")
            return render(request,'dairyapp/edit_fat.html',{'form':form})
            # else:
            #     # return HttpResponse("404")
            #     raise Http404("Poll does not exist")
            
@method_decorator(login_required(login_url='account_login'),name="dispatch")
@method_decorator(verified_dairy_user,name="dispatch")
class DeleteFatRate(DeleteView):
    print("delete view called")
    model = FatRate
    success_url = reverse_lazy("dairyapp:fat_list")

    def post(self, request, *args, **kwargs):
       
        self.object = self.get_object()
        print(self.object.dairy)
        if self.object.dairy.user == self.request.user:
            return super().post(self, request, *args, **kwargs)  
        raise PermissionDenied()
          

    # def get_queryset(self):
    #     return super().get_queryset().filter(id=self.kwargs['pk'],dairy__user=self.request.user)
    
       
#Dairy views
@method_decorator(login_required(login_url='account_login'),name="dispatch")
# @method_decorator(verified_dairy_user,name="dispatch")
class CreateDairyView(CreateView):
     model = Dairy
     form_class = CreateDairyForm
     template_name_suffix = '_create_form'

     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uid = uuid.uuid4()
        context['uid'] = uid
        print("uid",uid)
        return context

     def form_valid(self, form):
        """If the form is valid, save the associated model."""
        if self.request.user.has_verified_dairy:
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            return super().form_valid(form)
        raise BadRequest("please verify dairy")

@method_decorator(login_required(login_url='account_login'),name="dispatch") 
class UpadteDairyView(UpdateView):
     model = Dairy
     form_class = CreateDairyForm
     template_name = 'dairyapp/dairy_edit_form.html'
    

     def get_queryset(self):
          return super().get_queryset().filter(user=self.request.user)
    

@method_decorator(login_required(login_url='account_login'),name="dispatch")
@method_decorator(verified_dairy_user,name="dispatch")
class ListMilkRecords(ListView):
    model = MilkRecord
    context_object_name = "milkrecords"
    paginate_by = 16

    def paginate_queryset(self,queryset,page_size):
        try:
            return super().paginate_queryset(queryset,page_size)
        except Http404:
            self.kwargs['page'] = 1
            return super().paginate_queryset(queryset,page_size)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['start_date'] = is_valid_date(self.request.GET.get('start_date',"")) 
        context['end_date'] = is_valid_date(self.request.GET.get('end_date',""))
        context['shift'] =  self.request.GET.get('shift')
        context['date'] = is_valid_date( self.request.GET.get('date',""))
        context['dairy'] = self.kwargs['dairy']
        dairy = get_object_or_404(Dairy,slug=self.kwargs['dairy'],user=self.request.user)
        context['members'] = dairy.members.all()
        return context
    
    def get_queryset(self):
        request = self.request
        print("date",self.request.GET.get('date'))
        print("name",self.request.GET.get('name'))
        name = self.request.GET.get('name')
        shift = request.GET.get('shift')
        date = convert_nepali_date(request.GET.get('date',''))
        start_date = convert_nepali_date(request.GET.get('start_date',''))
        print("start_date",start_date)
        end_date = convert_nepali_date(request.GET.get('end_date',''))
        print("end_date",end_date)
        
        # return super().get_queryset() 
        
        dairy = get_object_or_404(Dairy,slug=self.kwargs['dairy'])
        queryset  = super().get_queryset() 
        filters = Q(dairy=dairy,dairy__user=self.request.user)
        
        if name:
            filters &= Q(user__first_name__icontains=name)

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


        # return super().get_queryset()
        dairy = get_object_or_404(Dairy,slug=self.kwargs['dairy'])
        return queryset.filter(filters)
        


@method_decorator(login_required(login_url='account_login'),name="dispatch")
@method_decorator(verified_dairy_user,name="dispatch")
class CreateMilkRercord(View):
    
    num = None
    def get(self,request,*args,**kwargs):
            """
            user can add milk record if he is verified user
            """
            try:
                num = int(request.GET.get('num'))
                if num <=0:
                    num = 1
            except Exception as e:
                print("inside except")
                print(e)
                num = 1
            print("&&&&&&&&&&&",num)
            
            CreateMilkRecordFormSet = modelformset_factory(MilkRecord,form=CreateMilkRecordForm,extra=num,max_num=30,edit_only=True,can_delete=True)
            print("============",request.GET.get('num'),0)
            try:
                print(kwargs['dairy'])
                dairy = Dairy.objects.get(slug=kwargs['dairy'],user=self.request.user)
                user = User.objects.get(id=kwargs['id'])
                print("dairy===============",dairy)
                
                formset = CreateMilkRecordFormSet(queryset=MilkRecord.objects.none(),form_kwargs={'dairy':dairy,'user':user,})

                # formset = self.CreateMilkRecordFormSet(initial=[
                #     {
                #         'user':user,
                #         'dairy':dairy
                #     }
                # ])
                    
                return render(request,'dairyapp/milkrecord_create.html',{'formset':formset,'user':user,'num':num})
                # else:
                #     print('inside else')
                #     #  raise HttpResponseForbidden("Sorry,")
                #     raise PermissionDenied()
            except Dairy.DoesNotExist:
                raise Http404
                 
            except User.DoesNotExist:
                raise Http404
        
        
    def post(self,request,*args,**kwargs):
            num = int(request.POST.get('num'))
                

            CreateMilkRecordFormSet = modelformset_factory(MilkRecord,form=CreateMilkRecordForm,extra=num,max_num=10,can_delete=True)
            print("inside mike record post methos")
            dairy =get_object_or_404(Dairy,slug=kwargs['dairy'],user=self.request.user)
            user = get_object_or_404(User,id=kwargs['id'])
            formset = CreateMilkRecordFormSet(request.POST,form_kwargs={'dairy':dairy,'user':user})
            if formset.is_valid():
                # print(request.POST)
                print("inside valid data")
                # milk_records  = formset.save(commit=False)
                formset.save()

                
                # for milk_record in formset.forms:
                
                #     new_record = milk_record.save(commit=False)
                #     new_record.dairy = dairy
                #     new_record.save()
                
                messages.success(request, _("Record added successfully"))
                return HttpResponseRedirect(reverse("dairyapp:member_milk_record",kwargs={'dairy':self.kwargs['dairy'],'id':self.kwargs['id']}))
            print("invalid form data++++++")
            print(formset)
            return render(request,'dairyapp/milkrecord_create.html',{'formset':formset,'num':num})

    
@method_decorator(login_required(login_url='account_login'),name="dispatch")
@method_decorator(verified_dairy_user,name="dispatch")
class UpdateMilkRercord(View):
    def get(self,request,*args,**kwargs):
            """
            user can add milk record if he is verified user
            """
            try:
                id = self.kwargs['id']
                print("id",id)
                
                dairy = Dairy.objects.get(slug=kwargs['dairy'],user=self.request.user)
                print("dairy",dairy)
                milkrecord = MilkRecord.objects.get(id=id)
                print("milkrec",milkrecord)
                # dairy =get_object_or_404(Dairy,name=kwargs['dairy'],user=self.request.user)
                print(dairy.members.all())
                form = UpdateMilkRecord(instance=milkrecord,initial={'dairy':dairy})
                
                return render(request,'dairyapp/milkrecord_edit.html',{'form':form})
            except Exception as e:
                print(e) 
                raise Http404("Page Not Found")
        
        
    def post(self,request,*args,**kwargs):
            id = self.kwargs['id']
            print("inside mike record post methos")
            dairy =get_object_or_404(Dairy,slug=kwargs['dairy'],user=self.request.user)
            milkrecord = MilkRecord.objects.get(id=id)
            form = UpdateMilkRecord(request.POST,instance = milkrecord)
            if form.is_valid():
                print(request.POST)
                print("inside valid data")
                miklrecord = form.save(commit=False)
                print("milkrec user",miklrecord.user)
                miklrecord.dairy = dairy
                miklrecord.save()
                return HttpResponseRedirect(reverse("dairyapp:milk_record",kwargs={'dairy':self.kwargs['dairy']}))
            return render(request,'dairyapp/milkrecord_edit.html',{'form':form})





@method_decorator(login_required(login_url='account_login'),name="dispatch")
@method_decorator(verified_dairy_user,name="dispatch")
class ListMemberMilkRecord(ListView):
    paginate_by = 16
    model = MilkRecord
    context_object_name = "milkrecords"
    template_name = "dairyapp/member_milkrecord_list.html"

    def paginate_queryset(self,queryset,page_size):
        try:
            return super().paginate_queryset(queryset,page_size)
        except Http404:
            self.kwargs['page'] = 1
            return super().paginate_queryset(queryset,page_size)


    # def paginate_queryset(self,queryset,page_size):
    #     try:
    #         return super(ListMemberMilkRecord,self).paginate_queryset(queryset,page_size)
    #     except Http404:
    #         self.kwargs['page'] = 1
    #         return super(ListMemberMilkRecord,self).paginate_queryset(queryset,page_size)

    

    

    

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['dairy'] = self.kwargs['dairy']
        context['id'] = self.kwargs['id']
        context['start_date'] = is_valid_date(self.request.GET.get('start_date',"")) 
        context['end_date'] = is_valid_date(self.request.GET.get('end_date',""))
        context['shift'] =  self.request.GET.get('shift')
        context['date'] = is_valid_date( self.request.GET.get('date',""))
        context['display'] = self.request.GET.get('display','d-none')
        context['count'] = self.kwargs['count']
        context['total_milk_wieght'] = self.kwargs['total_milk_wieght']
        context['avg_fat'] = round(self.kwargs['avg_fat'],3)
        context['total_price'] = self.kwargs['total_price']
        context['fat_rate'] = self.kwargs['fat_rate']
        context['bonous'] = self.kwargs['bonous']
        context['total_fat_rate'] = self.kwargs['total_fat_rate']
        dairy = get_object_or_404(Dairy,slug=self.kwargs['dairy'],user=self.request.user)
        context['members'] = dairy.members.all()
        

        
        return context
    
        
    
    # def get_fat_rate_fun(self,request,start_date,end_date,dairy,fat_rate_obj):
    #         print("inside get fat rate========")
                
    #         try:


    #             """
    #                 New Logic
    #             """
    #             if fat_rate_obj.count()>1:
    #                 #raise error if multiple fat range exists within date range
    #                 messages.error(request, _("Cannot apply filter witin date range. Multiple fat rate exists."))

    #             elif fat_rate_obj.count() == 1:
    #                 fat_rate = fat_rate_obj.first().get_fat_rate
    #                 self.kwargs['fat_rate'] = fat_rate_obj.first().fat_rate
    #                 self.kwargs['bonous'] = fat_rate_obj.first().bonous_amount
    #                 self.kwargs['total_fat_rate'] = fat_rate
    #                 print("fat rate===",fat_rate)
    #                 return fat_rate

    #             elif getFatBasedOnDate(start_date,end_date,dairy,self.request) is not None:
                    
    #                 print("inside first elif")
    #                 fat_rate_obj = getFatBasedOnDate(start_date,end_date,dairy,self.request)
    #                 fat_rate = fat_rate_obj.get_fat_rate
    #                 self.kwargs['fat_rate'] = fat_rate_obj.fat_rate
    #                 self.kwargs['bonous'] = fat_rate_obj.bonous_amount
    #                 self.kwargs['total_fat_rate'] = fat_rate
    #                 return fat_rate

    #             elif FatRate.objects.filter(dairy=dairy,dairy__user=self.request.user).order_by("created_at").exists():
    #                 fat_rate_obj = FatRate.objects.filter(dairy=dairy,dairy__user=self.request.user).order_by("created_at").first()
    #                 fat_rate = fat_rate_obj.get_fat_rate
    #                 self.kwargs['fat_rate'] = fat_rate_obj.fat_rate
    #                 self.kwargs['bonous'] = fat_rate_obj.bonous_amount
    #                 self.kwargs['total_fat_rate'] = fat_rate
    #                 return fat_rate
    #             else:
    #                 print("inside last else")
    #                 messages.error(request, _("Cannot fint fat rate witin date range.Fat rate doesnot exists."))
    #                 self.kwargs['fat_rate'] = 0
    #                 self.kwargs['bonous'] = 0
    #                 self.kwargs['total_fat_rate'] = 0
    #                 return 0
    #         except Exception as e:
    #             print("exception occour")
    #             return 0
    
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
            user = get_object_or_404(User,id=self.kwargs['id'])
            dairy = get_object_or_404(Dairy,slug=self.kwargs['dairy'])
            queryset  = super().get_queryset() 
            filters = Q(dairy=dairy,dairy__user=self.request.user,user=user)
            # return MilkRecord.objects.filter(dairy=dairy,dairy__user=self.request.user,user=user)


            print("dairy+++++++",dairy)
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
                for i in range(1,28):
                    date = f"2023-10-{i}"
                    if i<9:
                        date = f"2023-10-0{i}"
                    MilkRecord.objects.create(
                        dairy = dairy,
                        user = user,
                        shift = "morning",
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

            if shift and start_date and end_date:
                print("inside first if")
                
                if qs:
                    print("inside secode if")
                    # print("+++++++++++",getFatBasedOnDate(start_date,end_date))
                    """
                    perform qs operation if only qs is not empty
                    """
                
                    milk_wg = round(qs.aggregate(Sum("milk_weight")).get('milk_weight__sum'),3)
                    avg_fat = qs.aggregate(Avg("milk_fat")).get('milk_fat__avg')
                    self.kwargs['total_milk_wieght'] = milk_wg
                    self.kwargs['avg_fat'] = avg_fat
                    print("milk_weight",milk_wg)
                    print("average_fat",avg_fat)

                    fat_rate_obj = FatRate.objects.filter(dairy=dairy,dairy__user=self.request.user)
                    print("count obj---",fat_rate_obj.count())
                
                    
                    try:
                        print("inside try") 
                        if fat_rate_obj != 0:

                            total_price = get_fat_rate_fun(self,start_date=start_date,end_date=end_date,dairy=dairy,fat_rate_obj=fat_rate_obj)['fat_rate']*milk_wg*avg_fat
                        else:
                            toatl_price = 0
                    except Exception as e:
                        print("e==",e)
                        total_price = 0
                    self.kwargs['total_price'] = round(total_price,3)

                    # print("total price===",total_price)
                    


                
            return queryset.filter(filters).order_by('created_at')
        except Exception as e:
            print(e)
            raise BadRequest("Bad Request")
   
@method_decorator(login_required(login_url='account_login'),name="dispatch")
class DeleteMilkRecordView(View):
    def post(self,request,*args,**kwargs):
        dairy = get_object_or_404(Dairy,user=self.request.user)
        user = get_object_or_404(User,id=kwargs.get('userid'))
        milkrecord = get_object_or_404(MilkRecord,id=kwargs.get('milkid'))
        
        milkrecord.delete()
        return redirect("dairyapp:member_milk_record",id=user.id,dairy=dairy.slug)
        
        print(user)
        print(dairy)
    
    
@method_decorator(login_required(login_url='account_login'),name="dispatch")
class VerifyEsewa(View):
     def get(self,request):
        url ="https://uat.esewa.com.np/epay/transrec"
        q = request.GET.get('q')
        print(request.GET)
        

        d = {
            'amt':request.GET.get('amt'),
            'scd': 'EPAYTEST',
            'rid':  request.GET.get('refId'),
            'pid':request.GET.get('oid'),
        }
        resp = req.post(url, d)
        print("status code=====",resp.status_code)
        if resp.status_code == 200:
            user = self.request.user
            user.has_verified_dairy = True
            user.save()
        # print(resp.text)
            return HttpResponseRedirect(reverse('dairyapp:create_dairy'))
        else:
            raise Http404()
        





@method_decorator(login_required(login_url='account_login'),name="dispatch")
@method_decorator(verified_dairy_user,name="dispatch")
class ListDairyMembers(ListView):
    model = Dairy
    paginate_by=16
    template_name = 'dairyapp/list_dairy_members.html'
    context_object_name = 'members'

    def paginate_queryset(self,queryset,page_size):
        try:
            return super().paginate_queryset(queryset,page_size)
        except Http404:
            self.kwargs['page'] = 1
            return super().paginate_queryset(queryset,page_size)

    
    def get_queryset(self):
        # print("hello =========",super().get_queryset().filter(slug=self.kwargs.get('name')))
        qs = super().get_queryset().filter(user=self.request.user,slug=self.kwargs.get('dairy'))
        # print(qs[0].members.all)
        # print("outside if")
        # print("qs.count",qs.count())
        
        if qs.count() >= 1:
            # print("inside if----")
            # print(self.request)
            search = self.request.GET.get('name')
            # print("search",search)
            if search:
                result = qs[0].members.all().filter(Q(first_name__icontains=search))
                # print("qs",qs[0].members.all())
                # print("result",result)
                return result
            else:

                return qs[0].members.all()
        return qs
     
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        # print("context===",context)
        
        context['dairy'] = get_object_or_404(Dairy,slug=self.kwargs['dairy'],user=self.request.user)
        return context

from xhtml2pdf import pisa
from django.template.loader import get_template

@method_decorator(login_required(login_url='account_login'),name="dispatch")
@method_decorator(verified_dairy_user,name="dispatch")
class SendMilkReportEmialView(View):
    def get(self,request,*args,**kwargs):
        dairy_name = request.GET.get('dairy')
        start_date = convert_nepali_date(request.GET.get('start_date',''))
        end_date = convert_nepali_date(request.GET.get('end_date',''))
        shift = request.GET.get('shift')
        user_id = request.GET.get('id')

        print("start_date",start_date)
        print("end_date",end_date)

        
        

             
        user =  None
        dairy = None
        fat_rate = None

        if not start_date and not end_date:
            messages.error(request,_("Please select start date and end date"))
            return redirect('dairyapp:member_milk_record',dairy=dairy_name,id=user_id)

        try:
            try:
                dairy = Dairy.objects.get(slug=dairy_name,user=request.user)
            except Dairy.DoesNotExist:
                messages.error(request, _("Sorry,dairy with username doesnot exists."))
                return redirect("dairyapp:member_milk_record",id=user_id,dairy=dairy_name)
            
            
            
            fat_rate_obj = FatRate.objects.filter(dairy=dairy,dairy__user=self.request.user,created_at__range=(start_date,end_date))
            print("count obj---",fat_rate_obj.count())


            """
                New Logic
            """
            # if fat_rate_obj.count()>1:
            #     #raise error if multiple fat range exists within date range
            #     messages.error(request, _("Cannot apply filter witin date range. Multiple fat rate exists."))

            # elif fat_rate_obj.count() == 1:
            #     fat_rate = fat_rate_obj.first().get_fat_rate
            #     self.kwargs['fat_rate'] = fat_rate_obj.first().fat_rate
            #     self.kwargs['bonous'] = fat_rate_obj.first().bonous_amount
            #     self.kwargs['total_fat_rate'] = fat_rate
            #     print("fat rate===",fat_rate)

            # elif getFatBasedOnDate(start_date,end_date,dairy,self.request) != None:
                
            #     print("inside first elif")
            #     fat_rate_obj = getFatBasedOnDate(start_date,end_date,dairy,self.request)
            #     fat_rate = fat_rate_obj.get_fat_rate
            #     self.kwargs['fat_rate'] = fat_rate_obj.fat_rate
            #     self.kwargs['bonous'] = fat_rate_obj.bonous_amount
            #     self.kwargs['total_fat_rate'] = fat_rate

            # else:
            #     fat_rate_obj = FatRate.objects.filter(dairy=dairy,dairy__user=self.request.user).order_by("created_at").first()
            #     fat_rate = fat_rate_obj.get_fat_rate
            #     self.kwargs['fat_rate'] = fat_rate_obj.fat_rate
            #     self.kwargs['bonous'] = fat_rate_obj.bonous_amount
            #     self.kwargs['total_fat_rate'] = fat_rate

                
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                messages.error(request, _("Sorry,invalid userid"))
                return redirect("dairyapp:member_milk_record",id=user_id,dairy=dairy_name)
            
            morning_milk_records = MilkRecord.objects.filter(dairy__user=self.request.user,dairy=dairy,shift="morning",user=user,date__gte=start_date, date__lte=end_date)
            night_milk_records = MilkRecord.objects.filter(dairy__user=self.request.user,date__gte=start_date, date__lte=end_date,shift="night",user=user)

            milk_wg = 0
            avg_fat = 0
            nmilk_wg = 0
            navg_fat = 0
            

            if morning_milk_records.exists():
            
                milk_wg = morning_milk_records.aggregate(Sum("milk_weight")).get('milk_weight__sum')
                print("milk_wg",milk_wg)
            
                avg_fat = morning_milk_records.aggregate(Avg("milk_fat")).get('milk_fat__avg')

            
                
            fat_rate = get_fat_rate_fun(self,start_date=start_date,end_date=end_date,dairy=dairy,fat_rate_obj=fat_rate_obj)
            if night_milk_records.exists():
                nmilk_wg = night_milk_records.aggregate(Sum("milk_weight")).get('milk_weight__sum')
                navg_fat = night_milk_records.aggregate(Avg("milk_fat")).get('milk_fat__avg')
            
            if fat_rate:
                print("before nmilk_wg")
                
                total_price = fat_rate['fat_rate']*milk_wg*avg_fat
                nfat_rate = fat_rate['fat_rate']

                # print(f"nmilk_wg:{nmilk_wg} navg_fat:{navg_fat} nfat_rate:{nfat_rate}")

                if nmilk_wg is None:
                    nmilk_wg = 0

                if navg_fat is None:
                    navg_fat = 0
                
                print("fat_rate_=======",fat_rate)
                ntotal_price = fat_rate['fat_rate']*nmilk_wg*navg_fat


                context = {
                    'total_milk_wieght':milk_wg,
                    'avg_fat': round(avg_fat,3),
                    'fat_rate':round(fat_rate['fat_rate'],3),
                    'total_price':round(total_price,3),
                    'bonus':fat_rate['fat_rate_obj'].bonous_amount,


                    'ntotal_milk_wieght':nmilk_wg,
                    'navg_fat': round(navg_fat,3),
                    'nfat_rate':round(nfat_rate,3),
                    'ntotal_price':round(ntotal_price,3),
                    'dairy':dairy,


                    'user':user,
                    'shift':'morning',
                    'morning_milk_records':morning_milk_records,
                    'night_milk_records': night_milk_records
                }
                print("context===========",context)

            
                
                rendered_mail_template = render_to_string("dairyapp/email/report.html",context)


                print("rendered_mail_tem===========",rendered_mail_template)
                pdf = HTML(string=rendered_mail_template).write_pdf()
                # buffer = io.BytesIO()
                # html.write_pdf(target=buffer)
                # pdf = buffer.getvalue()


                filename = 'test.pdf'
                mimetype_pdf = 'application/pdf'
                

                # template_path = "dairyapp/email/report.html"
                # response = HttpResponse(content_type = 'application/pdf')
                # template = get_template(template_path)
                # html = template.render(context)
                # print(html)
                # pisa_status = pisa.CreatePDF(
                #     html,data=response
                # )
                # if pisa_status.err:
                #     return HttpResponse('error occoured')
                # return response


                try:

                    # sm.delay(
                    #     subject="Milk Report",
                    #     from_email=settings.EMAIL_HOST_USER,
                    #     to=user.email,
                    #     message="hello",
                    #     filename=filename,
                    #     pdf=pdf
                    # )
                    
                    sendMial(
                        subject="Milk Report",
                        from_email=settings.EMAIL_HOST_USER,
                        to=user.email,
                        message="hello",
                        filename=filename,
                        pdf=pdf)
                except Exception as e:
                    print(e)

                return HttpResponse(rendered_mail_template)
                messages.success(request,_("milk report email sent"))
                return redirect("dairyapp:member_milk_record",id=user_id,dairy=dairy_name)
            else:
                print("inside else man")
                return redirect("dairyapp:member_milk_record",id=user_id,dairy=dairy_name)
                

        except Exception as e:
            print("e----------",e)
            raise BadRequest("Bad Request")
            # return HttpResponseNotFound
            
# Create your views here.
def home(request):
    id = uuid.uuid4()
    print(id)
    return render(request,'myapp/index.html',{'uuid':id})

@method_decorator(login_required(login_url='account_login'),name="dispatch")
def initkhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    return_url = request.POST.get('return_url')
    purchase_order_id = request.POST.get('purchase_order_id')
    amount = request.POST.get('amount')

    print("return_url",return_url)
    print("purchase_order_id",purchase_order_id)
    print("amount",amount)
    user = request.user







    payload = json.dumps({
        "return_url": return_url,
        "website_url": "http://127.0.0.1:8000",
        "amount": amount,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": "test",
        "customer_info": {
        "name": user.first_name,
        "email": user.email,
        "phone": user.phone_number
        }
    })
    headers = {
        'Authorization': 'key b885cd9d8dc04eebb59e6f12190ae017',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    new_res = json.loads(response.text)
    print(new_res)
    return redirect(new_res['payment_url'])




    pass
    # url = "https://a.khalti.com/api/v2/epayment/initiate/"
    # return_url = request.POST.get('return_url')
    # website_url = request.POST.get('return_url')
    # amount = request.POST.get('amount')
    # purchase_order_id = request.POST.get('purchase_order_id')


    # print("url",url)
    # print("return_url",return_url)
    # print("web_url",website_url)
    # print("amount",amount)
    # print("purchase_order_id",purchase_order_id)
    # payload = json.dumps({
    #     "return_url": return_url,
    #     "website_url": website_url,
    #     "amount": amount,
    #     "purchase_order_id": purchase_order_id,
    #     "purchase_order_name": "test",
    #     "customer_info": {
    #     "name": "Bibek Dahal",
    #     "email": "test@khalti.com",
    #     "phone": "9800000001"
    #     }
    # })
    # headers = {
    #     'Authorization': 'key b885cd9d8dc04eebb59e6f12190ae017',
    #     'Content-Type': 'application/json',
    # }

    # response = requests.request("POST", url, headers=headers, data=payload)
    # print(json.loads(response.text))

    # print(response.text)
    # new_res = json.loads(response.text)
    # # print(new_res['payment_url'])
    # print(type(new_res))
    # return redirect(new_res['payment_url'])
    # return redirect("home")

@method_decorator(login_required(login_url='account_login'),name="dispatch")
def verifyKhalti(request):
    # print("url has been called")
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    if request.method == 'GET':
        headers = {
            'Authorization': 'key b885cd9d8dc04eebb59e6f12190ae017',
            'Content-Type': 'application/json',
        }
        pidx = request.GET.get('pidx')
        data = json.dumps({
            'pidx':pidx
        })
        res = requests.request('POST',url,headers=headers,data=data)
        print(res)
        print(res.text)

        new_res = json.loads(res.text)
        print(new_res)
        

        if new_res['status'] == 'Completed':
            user = request.user
            user.has_verified_dairy = True
            user.save()
        
        # else:
        #     # give user a proper error message
        #     raise BadRequest("sorry ")

        return redirect('dairyapp:create_dairy')





















    # print("url has been called")
    # url = "https://a.khalti.com/api/v2/epayment/lookup/"
    # if request.method == 'GET':
    #     headers = {
    #         'Authorization': 'key b885cd9d8dc04eebb59e6f12190ae017',
    #         'Content-Type': 'application/json',
    #     }
    #     pidx = request.GET.get('pidx')
    #     data = json.dumps({
    #         'pidx':pidx
    #     })
    #     res = requests.request('POST',url,headers=headers,data=data)
    #     print(res)
    #     print(res.text)

    #     new_res = json.loads(res.text)
    #     print(new_res)
        

    #     if new_res['status'] == 'Completed':
    #         user = request.user
    #         user.has_verified_dairy = True
    #         user.save()
        
    #     # else:
    #     #     # give user a proper error message
    #     #     raise BadRequest("sorry ")

    #     return redirect('dairyapp:create_dairy')
    
            
            
