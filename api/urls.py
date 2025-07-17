# urls.py

from rest_framework.routers import DefaultRouter
from .views import BookClassViewSet, BookingListViewSet, FitnessClassViewSet

router = DefaultRouter()
router.register(r'classes', FitnessClassViewSet, basename='class')      # Optional: GET /classes
router.register(r'book', BookClassViewSet, basename='book')             # POST /book/
router.register(r'bookings', BookingListViewSet, basename='bookings')   # GET /bookings/?email=

urlpatterns = router.urls
