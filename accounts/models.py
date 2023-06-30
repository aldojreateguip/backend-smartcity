from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password,check_password as django_check_password
# Create your models here.
class MPers(models.Model):
    pers_p_incodper = models.AutoField(db_column='PERS_P_inCODPER', primary_key=True)  # Field name made lowercase.
    pers_chnomper = models.CharField(db_column='PERS_chNOMPER', max_length=100)  # Field name made lowercase.
    pers_chapeper = models.CharField(db_column='PERS_chAPEPER', max_length=100)  # Field name made lowercase.
    pers_chdocide = models.CharField(db_column='PERS_chDOCIDE', max_length=20)  # Field name made lowercase.
    pers_chcelper = models.CharField(db_column='PERS_chCELPER', max_length=9)  # Field name made lowercase.
    pers_chemaper = models.CharField(db_column='PERS_chEMAPER', max_length=300)  # Field name made lowercase.
    dire_f_incodper = models.IntegerField(db_column='DIRE_F_inCODPER')  # Field name made lowercase.
    tipo_f_incodper = models.IntegerField(db_column='TIPO_F_inCODPER')  # Field name made lowercase.

    class Meta:
        db_table = 'm_pers'

class MUsua(models.Model):
    usua_p_incodusu = models.AutoField(db_column='USUA_P_inCODUSU', primary_key=True)  # Field name made lowercase.
    usua_chlogusu = models.CharField(db_column='USUA_chLOGUSU', max_length=50, unique=True)  # Field name made lowercase.
    usua_chpasusu = models.CharField(db_column='USUA_chPASUSU', max_length=200, default='')  # Field name made lowercase.
    tipo_f_incodusu = models.IntegerField(db_column='TIPO_F_inCODUSU')  # Field name made lowercase.
    pers_f_incodper = models.IntegerField(db_column='PERS_F_inCODPER')  # Field name made lowercase.

    USERNAME_FIELD = 'usua_chlogusu'
    REQUIRED_FIELDS = ['usua_chpasusu']
    class Meta:
        db_table = 'm_usua'
    
    def check_password(self, raw_password):
        return django_check_password(raw_password, self.usua_chpasusu)
    
    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def save(self, *args, **kwargs):
        if not self.pk:
            # Es un nuevo objeto, hasheamos la contraseña
            self.usua_chpasusu = make_password(self.usua_chpasusu)
        super().save(*args, **kwargs)

class STipoPers(models.Model):
    tipo_p_incodper = models.AutoField(db_column='TIPO_P_inCODPER', primary_key=True)  # Field name made lowercase.
    tipo_chnomper = models.CharField(db_column='TIPO_chNOMPER', max_length=50)  # Field name made lowercase.
    esta_f_incodest = models.IntegerField(db_column='ESTA_F_inCODEST')  # Field name made lowercase.

    class Meta:
        db_table = 's_tipo_pers'

class STipoUsua(models.Model):
    tipo_p_incodusu = models.AutoField(db_column='TIPO_P_inCODUSU', primary_key=True)  # Field name made lowercase.
    tipo_chnomusu = models.CharField(db_column='TIPO_chNOMUSU', max_length=50)  # Field name made lowercase.
    esta_f_incodest = models.IntegerField(db_column='ESTA_F_inCODEST')  # Field name made lowercase.

    class Meta:
        db_table = 's_tipo_usua'

class SDire(models.Model):
    dire_p_incodper = models.AutoField(db_column='DIRE_P_inCODPER', primary_key=True)  # Field name made lowercase.
    dire_chnomdir = models.CharField(db_column='DIRE_chNOMDIR', max_length=50)  # Field name made lowercase.
    esta_f_incodest = models.IntegerField(db_column='ESTA_F_inCODEST')  # Field name made lowercase.

    class Meta:
        db_table = 's_dire'


class SEsta(models.Model):
    esta_p_incodest = models.AutoField(db_column='ESTA_P_inCODEST', primary_key=True)  # Field name made lowercase.
    esta_chnomest = models.CharField(db_column='ESTA_chNOMEST', max_length=50)  # Field name made lowercase.

    class Meta:
        db_table = 's_esta'