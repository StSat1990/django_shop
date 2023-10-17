from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, DetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# models.py, admin.py, views.py, urls.py

# def home_page(request):
#     return HttpResponse("<h1>Hello</h1>")
from products.forms import FormModelForm
from products.models import ProductModel, CategoryModel, Cart

# class CustomLoginView(LoginView):
#     template_name = 'registration/login_css.html'
#     redirect_authenticated_user = True
#
#     def get_success_url(self):
#         return reverse_lazy('idex')

class IndexPageView(ListView):
    template_name = 'index.html'
    queryset = ProductModel.objects.all()
    context_object_name = 'products'

class ShopPageView(ListView):
    template_name = 'shop.html'
    queryset = ProductModel.objects.all()
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        qs = ProductModel.objects.all()
        q = self.request.GET.get('q')
        category = self.request.GET.get('category')

        if q:
            qs = qs.filter(title__icontains=q)

        if category:
            category_ids = category.split(',')
            qs = qs.filter(category__in=category_ids)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories'] = CategoryModel.objects.all

        return context

    def get_queryset(self):
        qs = ProductModel.objects.all()
        q = self.request.GET.get('q')
        category = self.request.GET.get('category')
        sort = self.request.GET.get('sort')

        if q:
            qs = qs.filter(title__icontains=q)

        if category:
            category_ids = category.split(',')
            qs = qs.filter(category__in=category_ids)

        if sort:
            if sort == 'price':
                qs = qs.order_by('price')
            elif sort == '-price':
                qs = qs.order_by('-price')

        return qs

class ShopDetailView(DetailView):
    template_name = 'shop-details.html'
    model = ProductModel
    context_object_name = 'products'

class AboutUsView(TemplateView):
    template_name = 'about.html'

def send_form(request):
    context = {}

    form = FormModelForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/')

    context['forms'] = form
    return render(request, 'forms.html', context)


@login_required
def add_products_to_user_card(request, pk):
    if request.method == 'POST':
        checker = ProductModel.objects.get(id=pk)

        if checker.product_amount >= int(request.POST.get('pr_count')):
            Cart.objects.create(user_id=request.user.id,
                                user_product=checker,
                                user_product_quantity=int(request.POST.get('pr_count'))).save()

            return redirect('/')

        else:
            return redirect(f'/product/{checker.id}')

def user_cart(request):
    cart = Cart.objects.filter(user_id=request.user.id)

    if request.method == 'POST':
        main_text = 'Новый заказ\n\n'

        for i in cart:
            main_text += f'Товар: {i.user_product}\n' \
                         f'Количество: {i.user_product_quantity}'
            # bot.send_message(791555605, main_text)
            cart.delete()
            return redirect('/')

    return render(request, 'user_cart.html', {'cart': cart})


def delete_exact_user_cart(request, pk):
    product_to_delete = ProductModel.objects.get(id=pk)

    Cart.objects.filter(user_id=request.user.id,
                        user_product=product_to_delete).delete()

    return redirect('/user_cart')


# Register user
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')
        else:
            return redirect('/')

    return render(request, 'account/signup.html')


