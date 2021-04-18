from django.urls import path, include
from PC.views import line_view, matrix_view, pc_view
import debug_toolbar

urlpatterns = [
    #    path('admin/', admin.site.urls),
    path('line', line_view),
    path('matrix', matrix_view),
    path('<int:line_length>/<int:row_count>/<str:elements>', pc_view),
    path('<int:line_length>/<int:row_count>', pc_view),
    path('<int:line_length>/<str:elements>', pc_view),
    path('<int:line_length>', pc_view),
    path('', pc_view),
    path('__debug__/', include(debug_toolbar.urls)),
]
