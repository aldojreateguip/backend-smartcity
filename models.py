# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class MReco(models.Model):
    reco_p_incodrec = models.AutoField(db_column='RECO_P_inCODREC', primary_key=True)  # Field name made lowercase.
    reco_chnomrec = models.CharField(db_column='RECO_chNOMREC', max_length=50)  # Field name made lowercase.
    reco_dtfecrec = models.DateTimeField(db_column='RECO_dtFECREC')  # Field name made lowercase.
    asig_f_incodveh = models.IntegerField(db_column='ASIG_F_inCODVEH')  # Field name made lowercase.
    pers_f_incodcho = models.IntegerField(db_column='PERS_F_inCODCHO')  # Field name made lowercase.
    pers_f_incodsup = models.IntegerField(db_column='PERS_F_inCODSUP')  # Field name made lowercase.
    ruta_f_incodrut = models.IntegerField(db_column='RUTA_F_inCODRUT')  # Field name made lowercase.
    hora_f_incodhor = models.IntegerField(db_column='HORA_F_inCODHOR')  # Field name made lowercase.
    turn_f_incodtur = models.IntegerField(db_column='TURN_F_inCODTUR')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'm_reco'


class MRuta(models.Model):
    ruta_p_incodrut = models.AutoField(db_column='RUTA_P_inCODRUT', primary_key=True)  # Field name made lowercase.
    ruta_chnomrut = models.CharField(db_column='RUTA_chNOMRUT', max_length=50)  # Field name made lowercase.
    esta_f_incodest = models.IntegerField(db_column='ESTA_F_inCODEST')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'm_ruta'


class MVehi(models.Model):
    vehi_p_incodveh = models.AutoField(db_column='VEHI_P_inCODVEH', primary_key=True)  # Field name made lowercase.
    vehi_chnomveh = models.CharField(db_column='VEHI_chNOMVEH', max_length=50)  # Field name made lowercase.
    vehi_chplaveh = models.CharField(db_column='VEHI_chPLAVEH', max_length=7)  # Field name made lowercase.
    tipo_f_incodveh = models.IntegerField(db_column='TIPO_F_inCODVEH')  # Field name made lowercase.
    tipo_p_incodcom = models.IntegerField(db_column='TIPO_P_inCODCOM')  # Field name made lowercase.
    marc_f_incodveh = models.IntegerField(db_column='MARC_F_inCODVEH')  # Field name made lowercase.
    mode_f_incodvehint = models.IntegerField(db_column='MODE_F_inCODVEHint')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'm_vehi'


class SDire(models.Model):
    dire_p_incodper = models.AutoField(db_column='DIRE_P_inCODPER', primary_key=True)  # Field name made lowercase.
    dire_chnomdir = models.CharField(db_column='DIRE_chNOMDIR', max_length=50)  # Field name made lowercase.
    esta_f_incodest = models.IntegerField(db_column='ESTA_F_inCODEST')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 's_dire'


class SEsta(models.Model):
    esta_p_incodest = models.AutoField(db_column='ESTA_P_inCODEST', primary_key=True)  # Field name made lowercase.
    esta_chnomest = models.CharField(db_column='ESTA_chNOMEST', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 's_esta'


class SGpss(models.Model):
    gpss_p_incodgps = models.AutoField(db_column='GPSS_P_inCODGPS', primary_key=True)  # Field name made lowercase.
    gpss_chimegps = models.CharField(db_column='GPSS_chIMEGPS', max_length=50)  # Field name made lowercase.
    esta_f_incodest = models.IntegerField(db_column='ESTA_F_inCODEST')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 's_gpss'


class SHora(models.Model):
    hora_p_incodhor = models.AutoField(db_column='HORA_P_inCODHOR', primary_key=True)  # Field name made lowercase.
    hora_chnomhor = models.CharField(db_column='HORA_chNOMHOR', max_length=50)  # Field name made lowercase.
    esta_f_incodest = models.IntegerField(db_column='ESTA_F_inCODEST')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 's_hora'


class SInci(models.Model):
    inci_p_incodinc = models.AutoField(db_column='INCI_P_inCODINC', primary_key=True)  # Field name made lowercase.
    inci_chnominc = models.CharField(db_column='INCI_chNOMINC', max_length=50)  # Field name made lowercase.
    esta_f_incodest = models.IntegerField(db_column='ESTA_F_inCODEST')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 's_inci'


class SMarc(models.Model):
    marc_p_incodveh = models.AutoField(db_column='MARC_P_inCODVEH', primary_key=True)  # Field name made lowercase.
    marc_chnomveh = models.CharField(db_column='MARC_chNOMVEH', max_length=50)  # Field name made lowercase.
    esta_f_incodest = models.IntegerField(db_column='ESTA_F_inCODEST')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 's_marc'


class SMode(models.Model):
    mode_p_incodveh = models.AutoField(db_column='MODE_P_inCODVEH', primary_key=True)  # Field name made lowercase.
    mode_chnommod = models.CharField(db_column='MODE_chNOMMOD', max_length=50)  # Field name made lowercase.
    esta_f_incodest = models.IntegerField(db_column='ESTA_F_inCODEST')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 's_mode'


class STipoComb(models.Model):
    tipo_p_incodcom = models.AutoField(db_column='TIPO_P_inCODCOM', primary_key=True)  # Field name made lowercase.
    tipo_chnomcom = models.CharField(db_column='TIPO_chNOMCOM', max_length=50)  # Field name made lowercase.
    esta_f_incodest = models.IntegerField(db_column='ESTA_F_inCODEST')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 's_tipo_comb'


class STipoVehi(models.Model):
    tipo_p_incodveh = models.AutoField(db_column='TIPO_P_inCODVEH', primary_key=True)  # Field name made lowercase.
    tipo_chnomveh = models.CharField(db_column='TIPO_chNOMVEH', max_length=50)  # Field name made lowercase.
    esta_f_incodest = models.IntegerField(db_column='ESTA_F_inCODEST')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 's_tipo_vehi'


class STurn(models.Model):
    turn_p_incodtur = models.AutoField(db_column='TURN_P_inCODTUR', primary_key=True)  # Field name made lowercase.
    turn_chnomtur = models.CharField(db_column='TURN_chNOMTUR', max_length=50)  # Field name made lowercase.
    esta_f_incodest = models.IntegerField(db_column='ESTA_F_inCODEST')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 's_turn'


class VAsigVehi(models.Model):
    asig_p_incodveh = models.AutoField(db_column='ASIG_P_inCODVEH', primary_key=True)  # Field name made lowercase.
    vehi_f_incodveh = models.IntegerField(db_column='VEHI_F_inCODVEH')  # Field name made lowercase.
    gpss_f_incodgps = models.IntegerField(db_column='GPSS_F_inCODGPS')  # Field name made lowercase.
    asig_dtfecins = models.DateTimeField(db_column='ASIG_dtFECINS', blank=True, null=True)  # Field name made lowercase.
    asig_dtfecdes = models.DateTimeField(db_column='ASIG_dtFECDES', blank=True, null=True)  # Field name made lowercase.
    esta_f_incodest = models.IntegerField(db_column='ESTA_F_inCODEST')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'v_asig_vehi'


class VGestInci(models.Model):
    gest_p_incodinc = models.AutoField(db_column='GEST_P_inCODINC', primary_key=True)  # Field name made lowercase.
    esta_f_incodest = models.IntegerField(db_column='ESTA_F_inCODEST')  # Field name made lowercase.
    gest_chdesinc = models.CharField(db_column='GEST_chDESINC', max_length=150, blank=True, null=True)  # Field name made lowercase.
    gest_bnimainc = models.CharField(db_column='GEST_bnIMAINC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hist_f_incodrec = models.IntegerField(db_column='HIST_F_inCODREC', blank=True, null=True)  # Field name made lowercase.
    inci_f_incodinc = models.IntegerField(db_column='INCI_F_inCODINC', blank=True, null=True)  # Field name made lowercase.
    gest_dtfecinc = models.DateTimeField(db_column='GEST_dtFECINC', blank=True, null=True)  # Field name made lowercase.
    gest_chpunpar = models.CharField(db_column='GEST_chPUNPAR', max_length=100, blank=True, null=True)  # Field name made lowercase.
    gest_chpunfin = models.CharField(db_column='GEST_chPUNFIN', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'v_gest_inci'


class VHistReco(models.Model):
    hist_p_incodrec = models.AutoField(db_column='HIST_P_inCODREC', primary_key=True)  # Field name made lowercase.
    hist_dthorreg = models.DateTimeField(db_column='HIST_dtHORREG')  # Field name made lowercase.
    hist_chlatrec = models.CharField(db_column='HIST_chLATREC', max_length=100)  # Field name made lowercase.
    hist_chlongrec = models.CharField(db_column='HIST_chLONGREC', max_length=100)  # Field name made lowercase.
    hist_chvelrec = models.CharField(db_column='HIST_chVELREC', max_length=100)  # Field name made lowercase.
    hist_chdisrec = models.CharField(db_column='HIST_chDISREC', max_length=100)  # Field name made lowercase.
    hist_chtiedet = models.CharField(db_column='HIST_chTIEDET', max_length=100)  # Field name made lowercase.
    hist_dtfecreg = models.DateTimeField(db_column='HIST_dtFECREG')  # Field name made lowercase.
    reco_f_incodrec = models.IntegerField(db_column='RECO_F_inCODREC')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'v_hist_reco'


class VRutaCoor(models.Model):
    ruta_p_incodcoo = models.AutoField(db_column='RUTA_P_inCODCOO', primary_key=True)  # Field name made lowercase.
    ruta_chnomcoo = models.CharField(db_column='RUTA_chNOMCOO', max_length=50)  # Field name made lowercase.
    ruta_p_incodrut = models.IntegerField(db_column='RUTA_P_inCODRUT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'v_ruta_coor'
