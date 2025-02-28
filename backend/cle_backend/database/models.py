from django.db import models
from django.core.validators import MaxValueValidator
from datetime import datetime, date
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

AREA_TEMATICA_CHOICES = [
    ('durabilidad', 'Durabilidad'),
    ('ensayos_mecanicos', 'Ensayos Mecánicos'),
    ('geologia', 'Geología'),
    ('hormigones', 'Hormigones'),
    ('metalurgia', 'Metalurgia'),
    ('patrimonio', 'Patrimonio'),
    ('quimica', 'Química'),
    ('tecnologia_vial', 'Tecnología Vial'),
    ('estudios_especiales', 'Estudios Especiales'),
    ('servicios_tecnologicos', 'Servicios Tecnológicos'),  
    ('direccion', 'Dirección'),  
]

DESCUENTO_CHOICES = [
        (0, '0%'),
        (5, '5%'),
        (10, '10%'),
        (15, '15%'),
        (20, '20%'),
        (25, '25%'),
        (30, '30%'),
        (40, '40%'),
        (50, '50%'),
        (60, '60%'),
        (70, '70%'),
        (80, '80%'),
        (90, '90%'),
        (100, '100%'),
    ]

ESTADO_PRESUPUESTO_CHOICES = [
        ('en_espera', 'En Espera'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
        ('modificado', 'Modificado'),
        ('actualizado', 'Actualizado'),
    ]

ESTADO_RECEPCION_CHOICES = [
        ('sin_llegar','Sin LLegar'),
        ('parcial', 'Parcial'),
        ('total', 'Total'),
    ]

PAGO_CHOICES = [
        (0, '0%'),
        (50, '50%'),
        (100, '100%'),
]

ESTADO_INFORME_AREA_CHOICES = [
        ('sin_informe','Sin Informe'),
        ('parcial', 'Parcial'),
        ('total', 'Total'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    area_tematica = models.CharField(choices=AREA_TEMATICA_CHOICES, max_length=50)
    rol = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - {self.get_area_tematica_display()} - {self.rol}"

    # Crear o actualizar la señal para crear o guardar el UserProfile automáticamente cuando se crea o guarda un User

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
        else:
            # Solo actualiza el perfil si el usuario ya existe
            if hasattr(instance, 'userprofile'):
                instance.userprofile.save()

class Solicitante(models.Model):
    nro_solicitante = models.AutoField(primary_key=True)
    nombre_solicitante = models.CharField(max_length=255)
    cuit = models.CharField(max_length=20)
    pais = models.CharField(max_length=50)
    provincia = models.CharField(max_length=50)
    localidad = models.CharField(max_length=50)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    codigoPostal = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre_solicitante

class Presupuesto(models.Model):
    nro_presupuesto = models.AutoField(primary_key=True)
    fecha_presupuesto = models.DateField()
    contacto = models.CharField(max_length=100)
    telefono2 = models.CharField(max_length=20, null=True, blank=True)
    email2 = models.EmailField(max_length=50, null=True, blank=True)
    area_tematica = models.CharField(choices=AREA_TEMATICA_CHOICES)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.IntegerField(choices=DESCUENTO_CHOICES)
    arancel_presupuesto = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.TextField(max_length=255, null=True, blank=True)
    estado_presupuesto = models.CharField(choices=ESTADO_PRESUPUESTO_CHOICES)
    nro_solicitante = models.ForeignKey('Solicitante', on_delete=models.PROTECT)

    def __str__(self):
        return f"Presupuesto #{self.nro_presupuesto} - Solicitante: {self.nro_solicitante.nombre_solicitante}, Área Temática: {self.get_area_tematica_display()}"

    @property
    def detalles_presupuesto(self):
        return DetallePresupuesto.objects.filter(nro_presupuesto=self)
    
class Servicio(models.Model):
    nro_servicio = models.AutoField(primary_key=True)
    servicio = models.CharField(max_length=255)
    norma = models.CharField(max_length=255)
    arancel = models.IntegerField(validators=[MaxValueValidator(999999)])
    area_tematica = models.CharField(choices=AREA_TEMATICA_CHOICES)
    modulo = models.IntegerField(validators=[MaxValueValidator(999999)], default=275)
    

    def __str__(self):
        return f"Servicio #{self.nro_servicio} - {self.servicio}"

class DetallePresupuesto(models.Model):
    nro_detalle = models.AutoField(primary_key=True)
    nro_presupuesto = models.ForeignKey('Presupuesto', on_delete=models.CASCADE)
    nro_servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE)
    cant = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle #{self.nro_detalle} - Presupuesto #{self.nro_presup.nro_presup} - Servicio #{self.nro_servicio.nro_servicio}"
    
class DataServicio(models.Model):
    nro_dataServicio = models.AutoField(primary_key=True)
    fecha_dataServicio = models.DateField()
    adjunto_solicitudServicio = models.FileField(upload_to='solicitudes_servicio/', null=True)
    obra = models.CharField(max_length=255, null=True, blank=True)
    plazo_estimado = models.IntegerField() 
    cant_numLabs = models.IntegerField()
    muestras = models.TextField()
    observaciones = models.TextField(max_length=255, null=True, blank=True)
    nro_presupuesto = models.ForeignKey('Presupuesto', on_delete=models.CASCADE)
    completo = models.BooleanField(default=False) #Si es True habilito a adjuntar adjunto_solicitudServicio
    nro_circuito = models.ForeignKey('Circuito', on_delete=models.SET_NULL, null=True)
    finalizado = models.BooleanField(default=False)

    def __str__(self):
        return f"DataServicio #{self.nro_dataServicio} - Presupuesto #{self.nro_presupuesto.nro_presupuesto} - Legajo #{self.nro_legajo.nro_legajo}"

class Legajo(models.Model):
    nro_legajo = models.AutoField(primary_key=True)
    fecha_legajo = models.DateField()
    rangos_laboratorios = models.CharField(max_length=255)
    pago = models.CharField(choices=PAGO_CHOICES)
    plazo_pago = models.IntegerField(default=30)
    adjunto_factura = models.FileField(upload_to='facturas/', null=True)
    completo = models.BooleanField(default=False)
    nro_circuito = models.ForeignKey('Circuito', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Legajo #{self.nro_legajo} - DataServicio #{self.nro_dataServicio.nro_dataServicio}"

class Recepcion(models.Model):
    nro_recepcion = models.AutoField(primary_key=True)
    nros_remitos = models.CharField(max_length=255, null=True, blank=True)
    estado_recepcion = models.CharField(choices=ESTADO_RECEPCION_CHOICES, default='sin_llegar')
    plazo_muestras = models.IntegerField(default=30)
    completo = models.BooleanField(default=False)
    nro_circuito = models.ForeignKey('Circuito', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Recepcion #{self.nro_recepcion} - Legajo #{self.nro_legajo.nro_legajo}"

class OrdenServicio(models.Model):
    nro_ordenServicio = models.AutoField(primary_key=True)
    fecha_ordenServicio = models.DateField()
    observaciones = models.TextField(max_length=255, null=True, blank=True)
    completo = models.BooleanField(default=False)
    nro_circuito = models.ForeignKey('Circuito', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"OrdenServicio #{self.nro_ordenServicio} - Legajo #{self.nro_legajo.nro_legajo}"

class InformeArea(models.Model):
    nro_informeArea = models.AutoField(primary_key=True)
    fecha_informeArea = models.DateField()
    adjunto_informeArea = models.FileField(upload_to='informes_areas/')
    registros_ensayo = models.FileField(upload_to='registros_ensayo/', null=True)
    completo = models.BooleanField(default=False)
    estado_informeArea = models.CharField(choices=ESTADO_INFORME_AREA_CHOICES, default='sin_informe')
    nro_circuito = models.ForeignKey('Circuito', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"InformeArea #{self.nro_informeArea} - OrdenServicio #{self.nro_ordenServicio.nro_ordenServicio}"

class InformeAreaParcial(models.Model):
    informe_area = models.ForeignKey(
        InformeArea,
        related_name='informes_parciales',
        on_delete=models.CASCADE  # Borra los informes parciales si se elimina el InformeArea
    )
    fecha_parcial = models.DateField(auto_now_add=True)
    adjunto_parcial = models.FileField(upload_to='informes_parciales/')
    nro_circuito = models.ForeignKey('Circuito', on_delete=models.SET_NULL, null=True)


class InformeServicio(models.Model):
    nro_informeServicio = models.AutoField(primary_key=True)
    fecha_informeServicio = models.DateField(default=date.today)
    adjunto_informeServicio = models.FileField(upload_to='informes_servicio/')
    corregir = revision = models.BooleanField(default=False)
    revision = models.BooleanField(default=False)
    correcciones = models.TextField(max_length=2500, null=True, blank=True)
    # fecha_revision = models.DateField(null=True, blank=True)
    firma_area = models.BooleanField(default=False)
    # fecha_firmaArea = models.DateField(null=True, blank=True)
    firma_direccion = models.BooleanField(default=False)
    # fecha_firmaDireccion= models.DateField(null=True, blank=True)
    completo = models.BooleanField(default=False)
    nro_circuito = models.ForeignKey('Circuito', on_delete=models.SET_NULL, null=True)
    

    def __str__(self):
        return f"InformeServicio #{self.nro_informeServicio} - InformeArea #{self.nro_informeArea.nro_informeArea}"

class SolicitudInterarea(models.Model):
    nro_solicitudInterarea = models.AutoField(primary_key=True)
    fecha_solicitudInterarea = models.DateField()
    areaTematica_origen = models.CharField(choices=AREA_TEMATICA_CHOICES)
    inter_areaTematica = models.CharField(choices=AREA_TEMATICA_CHOICES)
    muestras_solicitudIa = models.TextField()
    num_labs = models.CharField(null=True, blank=True)
    observaciones = models.TextField(max_length=255, null=True, blank=True)
    nro_circuito = models.ForeignKey('Circuito', on_delete=models.SET_NULL, null=True)
    completo = models.BooleanField(default=False)

    def __str__(self):
        return f"SolicitudInterarea #{self.nro_solicitudInterarea} - InformeInterarea #{self.nro_informeInterarea.nro_informeInterarea}"

class DetalleInterarea(models.Model):
    nro_detalle = models.AutoField(primary_key=True)
    nro_solicitudInterarea = models.ForeignKey('SolicitudInterarea', on_delete=models.CASCADE)
    nro_servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE)
    cant = models.IntegerField()

    def __str__(self):
        return f"DetalleInterarea #{self.nro_detalle} - SolicitudInterarea #{self.nro_solicitudInterarea.nro_solicitudInterarea} - Servicio #{self.nro_servicio.nro_servicio}"

class InformeInterarea(models.Model):
    nro_informeInterarea = models.AutoField(primary_key=True)
    fecha_informeInterarea = models.DateField()
    # area_tematica = models.CharField(choices=AREA_TEMATICA_CHOICES)
    adjunto_informeInterarea = models.FileField(upload_to='informes_interarea/')
    nro_solicitudInterarea = models.ForeignKey('SolicitudInterarea', on_delete=models.CASCADE)
    nro_circuito = models.ForeignKey('Circuito', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"InformeInterarea #{self.nro_informeInterarea} - SolicitudInterarea #{self.nro_solicitudInterarea.nro_solicitudInterarea}"
    
class Circuito(models.Model):
    nro_circuito = models.AutoField(primary_key=True)
    finalizado = models.BooleanField(default=False)


class UltimoNumero(models.Model):
    anio = models.IntegerField(default=datetime.now().year)
    ultimo_numero = models.IntegerField(default=0)

    @classmethod
    def obtener(cls):
        """Obtiene el objeto de UltimoNumero para el año actual, o crea uno nuevo si no existe."""
        anio_actual = datetime.now().year
        obj, created = cls.objects.get_or_create(anio=anio_actual, defaults={'ultimo_numero': 0})
        obj._check_and_reset_anio()
        return obj

    @property
    def ultimo_numero_actual(self):
        """Devuelve el último número actual, ajustado si es necesario."""
        self._check_and_reset_anio()
        return self.ultimo_numero

    @ultimo_numero_actual.setter
    def ultimo_numero_actual(self, value):
        """Actualiza el último número y guarda el objeto."""
        self.ultimo_numero = value
        self.save()

    def _check_and_reset_anio(self):
        """Reinicia el número si cambia el año."""
        anio_actual = datetime.now().year
        if self.anio != anio_actual:
            self.anio = anio_actual
            self.ultimo_numero = 0
            self.save()

class Modulo(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    valor = models.IntegerField(default=1000)

    @classmethod
    def obtener_ultimo_modulo(cls):
        return cls.objects.latest('fecha')  # Obtiene la última instancia basada en la fecha

    @classmethod
    def actualizar_modulo(cls, nuevo_valor):
        # Crea una nueva instancia con el nuevo valor
        cls.objects.create(valor=nuevo_valor)

# Clases singleton que podria borrar
# class UltimoNumeroSingleton:
#     _instance = None
#     _ultimo_numero = None
#     _ultimo_anio = None

#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super().__new__(cls)
#             # Inicializar el último número y año aquí
#             cls._ultimo_numero = 0
#             cls._ultimo_anio = datetime.now().year  # Obtener el año actual al inicializar
#         return cls._instance
    
#     @property
#     def ultimo_numero(self):
#         return self._ultimo_numero

#     @ultimo_numero.setter
#     def ultimo_numero(self, value):
#         self._ultimo_numero = value

#     def _check_and_reset_anio(self):
#         anio_actual = datetime.now().year
#         if self._ultimo_anio != anio_actual:
#             self._ultimo_anio = anio_actual
#             self._ultimo_numero = 0 # Reiniciar el último número si cambia el año
    
# class ModuloHistory(models.Model):
#     valor = models.IntegerField()
#     fecha_cambio = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"{self.valor} - {self.fecha_cambio}"

# class Modulo:
#     _instance = None

#     def __new__(cls, *args, **kwargs):
#         if not cls._instance:
#             cls._instance = super(Modulo, cls).__new__(cls, *args, **kwargs)
#             cls._instance._initialize()
#         return cls._instance

#     def _initialize(self):
#         if not hasattr(self, 'valor'):
#             # Aquí puedes inicializar desde la base de datos si lo deseas
#             self.valor = 1000  # Valor inicial
#             self.registrar_cambio(self.valor)

#     def obtener_valor(self):
#         return self.valor

#     def actualizar_valor(self, nuevo_valor):
#         self.valor = nuevo_valor
#         self.registrar_cambio(nuevo_valor)

#     def registrar_cambio(self, valor):
#         ModuloHistory.objects.create(valor=valor)

#     def __str__(self):
#         return f"Modulo(value={self.valor})"