from django.db import models

# Create your models here.

from django.utils.timezone import now


class WXData(models.Model):
    site_info = models.CharField(max_length=255, db_column='SiteInfo')  # Mapping to the 'SiteInfo' column
    timestamp = models.DateTimeField(default=now, db_column='TimeStamp', primary_key=True)  # Primary Key

    # Define separate fields for each type of data
    lvl_ft_avg = models.FloatField(db_column='Lvl_ft_Avg')  # Water Level (Avg)
    cond_avg = models.FloatField(db_column='Cond_Avg')  # Conductivity (Avg)
    t_avg = models.FloatField(db_column='T_Avg')  # T (Avg) column

    def __str__(self):
        return f"{self.site_info} - {self.timestamp}"

    class Meta:
        app_label = 'dashboard'
        db_table = 'Data'  # Ensuring the table name is 'Data'
