from django.db import models

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
        managed = False
        db_table = 'm_pers'

class MUsua(models.Model):
    usua_p_incodusu = models.AutoField(db_column='USUA_P_inCODUSU', primary_key=True)  # Field name made lowercase.
    usua_chlogusu = models.CharField(db_column='USUA_chLOGUSU', max_length=50)  # Field name made lowercase.
    usua_chpasusu = models.CharField(db_column='USUA_chPASUSU', max_length=200)  # Field name made lowercase.
    tipo_f_incodusu = models.IntegerField(db_column='TIPO_F_inCODUSU')  # Field name made lowercase.
    pers_f_incodper = models.IntegerField(db_column='PERS_F_inCODPER')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'm_usua'

class STipoPers(models.Model):
    tipo_p_incodper = models.AutoField(db_column='TIPO_P_inCODPER', primary_key=True)  # Field name made lowercase.
    tipo_chnomper = models.CharField(db_column='TIPO_chNOMPER', max_length=50)  # Field name made lowercase.
    esta_f_incodest = models.IntegerField(db_column='ESTA_F_inCODEST')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 's_tipo_pers'

class STipoUsua(models.Model):
    tipo_p_incodusu = models.AutoField(db_column='TIPO_P_inCODUSU', primary_key=True)  # Field name made lowercase.
    tipo_chnomusu = models.CharField(db_column='TIPO_chNOMUSU', max_length=50)  # Field name made lowercase.
    esta_f_incodest = models.IntegerField(db_column='ESTA_F_inCODEST')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 's_tipo_usua'