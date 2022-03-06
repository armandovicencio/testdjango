from django.urls import path
from .views import WishesView, IndexView, WishesAdd,WishesEdit,WishDestroy,WishLike,WishGranted,WhishStats
app_name = "wishes"

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('wishes', WishesView.as_view(), name="wishes"),
    path('wishes/add', WishesAdd.as_view(), name="add"),
    path('wishes/edit/<int:pk>', WishesEdit.as_view(), name="edit"),
    path('wishes/<int:pk>/destroy', WishDestroy.as_view(), name="destroy"),
    path('wishes/<int:pk>/like', WishLike.as_view(), name="like"),
    path('wishes/<int:pk>/granted', WishGranted.as_view(), name="granted"),
    path('wishes/stats', WhishStats.as_view(), name="stats"),

]