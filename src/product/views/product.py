
from django.shortcuts import render
from django.views import generic, View 
from product.models import Variant, Product

import json

from product.utils import createProduct, createProductVarient,createProductVariantPrice

class  CreateProductView(View):

    def get(self, request):

        context = {}
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        

        return render (request,'products/create.html', context )

    def post(self, request):

        data = json.loads(request.body)

        product =createProduct(data)

        variants_obj_dict = createProductVarient(data, product)


        createProductVariantPrice(data, variants_obj_dict, product)

        context = {}
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())

        return render (request,'products/create.html', context )


class ProductView(generic.ListView):
    template_name = "products/list.html"
    paginate_by = 2
    model = Product
    context_object_name = "products"    

    def get_queryset(self):
        filter_string = {}
        for key in self.request.GET:
            if self.request.GET.get(key) and key != "page":   # exludes pagination parameter page
                filter_string[key] = self.request.GET.get(key)
        print("filter_string", filter_string)
        return Product.objects.filter(**filter_string).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        variants = Variant.objects.all()
        context["variants"] = variants

        #  to  add  query parameter  in pagination 
        queyr_paremeter = self.request.GET.copy()
        parameters = queyr_paremeter.pop('page', True) and queyr_paremeter.urlencode()
        context["parameters"] = parameters
        
        return context
