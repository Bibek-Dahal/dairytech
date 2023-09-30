from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from dairyapp.models import Dairy, FatRate, MilkRecord

from django.db.models import Q
from django.db.models import Avg,Sum
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from utils.dairyapp.commonutils import getFatBasedOnDate



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
    template_name = "user/member_milkrecord_list.html"
    paginate_by = 16

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['dairy'] = self.kwargs['dairy']
        # context['id'] = self.kwargs['id']
        context['start_date'] = self.request.GET.get('start_date')
        context['end_date'] = self.request.GET.get('end_date')
        context['shift'] = self.request.GET.get('shift')
        context['date'] = self.request.GET.get('date')
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
        request = self.request
        print("date",self.request.GET.get('date'))
        print("name",self.request.GET.get('name'))
        shift = request.GET.get('shift')
        date = request.GET.get('date')
        start_date = request.GET.get('start_date')
        print("start_date",start_date)
        end_date = request.GET.get('end_date')
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

        if shift:
            print("inside first if")
            if qs:
                print("inside secode if")
                print("inside secode if")
                # print("+++++++++++",getFatBasedOnDate(start_date,end_date).get_fat_rate)
                """
                perform qs operation if only qs is not empty
                """
            
                milk_wg = qs.aggregate(Sum("milk_weight")).get('milk_weight__sum')
                avg_fat = qs.aggregate(Avg("milk_fat")).get('milk_fat__avg')
                self.kwargs['total_milk_wieght'] = milk_wg
                self.kwargs['avg_fat'] = avg_fat
                print("milk_weight",milk_wg)
                
                print("average_fat",avg_fat)
                if start_date and end_date:
                    fat_rate_obj = FatRate.objects.filter(dairy=dairy,created_at__date__lte=end_date,created_at__date__gte=start_date)
                    print('fat rate obj count',fat_rate_obj.count())
                    if fat_rate_obj.count()>1:
                        messages.error(request, _("Cannot apply filter witin date range. Multiple fat rate exists."))
                        
                        # return redirect("dairyapp:member_milk_record",id=user.id,dairy=dairy.name)
                    elif fat_rate_obj.count() == 0:
                       
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
                    if fat_rate_obj.count()==1:
                        total_price = fat_rate*milk_wg*avg_fat
                except Exception as e:
                    total_price = 0
                self.kwargs['total_price'] = total_price
                # print("total price==",total_price)
                pass


             
        return queryset.filter(filters)