
from product.models import Product,Variant, ProductVariant, ProductVariantPrice

def createProduct( data):
        
    try:
        product = Product(title = data["title"],sku= data["sku"],description= data['description'])

        product.save()
    except:
        return None

    return product


def createProductVarient(data, product):

    variants_obj_dict = {}


    try:
        for variant in data["product_variant"]:
            for tag  in  variant['tags']:
                varient_obj = Variant.objects.get(id = variant["option"] )
                productVariant_obj = ProductVariant(variant_title = tag,variant = varient_obj ,product = product)
                productVariant_obj.save()
                variants_obj_dict[tag] = productVariant_obj
    except: 
        pass

    return variants_obj_dict


def createProductVariantPrice(data, variants_obj_dict, product):

    try:
        for product_variant_price in data["product_variant_prices"]:
            title_list = [i for i in product_variant_price["title"].split("/") if i != ""]


            product_variant_one = None
            product_variant_two  = None
            product_variant_three = None

            for title  in title_list:
                if variants_obj_dict[title].variant.id == 1:
                    product_variant_one = variants_obj_dict[title]
                elif variants_obj_dict[title].variant.id == 2:
                    product_variant_two = variants_obj_dict[title]
                elif variants_obj_dict[title].variant.id == 3:
                    product_variant_three = variants_obj_dict[title] 
                
            productVariantPrice_obj =  ProductVariantPrice(product_variant_one= product_variant_one, product_variant_two=product_variant_two,product_variant_three = product_variant_three,price=product_variant_price["price"] ,stock=product_variant_price["stock"],product  = product )  
            productVariantPrice_obj.save()
    except:
        pass
