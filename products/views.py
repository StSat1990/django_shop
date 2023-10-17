from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, DetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories'] = CategoryModel.objects.all()
        context['cart'] = Cart.objects.filter(user_id=self.request.user.id)

        return context


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
def add_to_cart(request, pk):
    if request.method == 'POST':
        checker = ProductModel.objects.get(id=pk)
        pr_count = request.POST.get('pr_count')

        if pr_count is not None:
            try:
                pr_count = int(pr_count)
                if pr_count < 1:
                    pr_count = 1  # Если указано отрицательное или нулевое значение, устанавливаем 1
            except ValueError:
                pr_count = 1  # Если не удается преобразовать в int, устанавливаем 1
        else:
            pr_count = 1  # Если pr_count отсутствует, устанавливаем 1 по умолчанию

        if checker.product_amount >= pr_count:
            Cart.objects.create(user_id=request.user.id,
                                user_product=checker,
                                user_product_quantity=pr_count)
        else:
            messages.error(request, 'Недостаточно товара.')

    return redirect('shop')


@login_required
def user_cart(request):
    cart = Cart.objects.filter(user_id=request.user.id)

    if request.method == 'POST':
        main_text = 'Новый заказ\n\n'

        for item in cart:
            main_text += f'Товар: {item.user_product}\n' \
                         f'Количество: {item.user_product_quantity}\n'

        # Здесь вы можете отправить уведомление о заказе

        cart.delete()
        return redirect('shop')

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


