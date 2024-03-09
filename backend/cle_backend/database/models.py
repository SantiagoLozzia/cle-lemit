from django.db import models
from django.core.validators import MaxValueValidator

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
    telefono2 = models.CharField(max_length=20, null=True)
    email2 = models.EmailField(max_length=50, null=True)
    area_tematica = models.CharField(choices=AREA_TEMATICA_CHOICES)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.IntegerField(choices=DESCUENTO_CHOICES)
    arancel_presupuesto = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.TextField(max_length=255, null=True)
    estado_presupuesto = models.CharField(choices=ESTADO_PRESUPUESTO_CHOICES)
    nro_solicitante = models.ForeignKey('Solicitante', on_delete=models.PROTECT)

    def __str__(self):
        return f"Presupuesto #{self.nro_presupuesto} - Solicitante: {self.nro_solicitante.nombre_solicitante}, Área Temática: {self.get_area_tematica_display()}"

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
    obra = models.CharField(max_length=255, null=True)
    plazo_estimado = models.IntegerField() 
    cant_numLabs = models.IntegerField()
    muestras = models.TextField()
    observaciones = models.TextField(max_length=255, null=True)
    nro_presupuesto = models.ForeignKey('Presupuesto', on_delete=models.CASCADE)
    completo = models.BooleanField(default=False)
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
    nros_remitos = models.CharField(max_length=255)
    estado_recepcion = models.CharField(choices=ESTADO_RECEPCION_CHOICES, default='sin_llegar')
    plazo_muestras = models.IntegerField(default=30)
    completo = models.BooleanField(default=False)
    nro_circuito = models.ForeignKey('Circuito', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Recepcion #{self.nro_recepcion} - Legajo #{self.nro_legajo.nro_legajo}"

class OrdenServicio(models.Model):
    nro_ordenServicio = models.AutoField(primary_key=True)
    fecha_ordenServicio = models.DateField()
    observaciones = models.TextField(max_length=255, null=True)
    completo = models.BooleanField(default=False)
    nro_circuito = models.ForeignKey('Circuito', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"OrdenServicio #{self.nro_ordenServicio} - Legajo #{self.nro_legajo.nro_legajo}"

class InformeArea(models.Model):
    nro_informeArea = models.AutoField(primary_key=True)
    fecha_informeArea = models.DateField()
    adjunto_informeArea = models.FileField(upload_to='informes_areas/')
    completo = models.BooleanField(default=False)
    estado_informeArea = models.CharField(choices=ESTADO_INFORME_AREA_CHOICES, default='sin_informe')
    nro_circuito = models.ForeignKey('Circuito', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"InformeArea #{self.nro_informeArea} - OrdenServicio #{self.nro_ordenServicio.nro_ordenServicio}"
    
class InformeServicio(models.Model):
    nro_informeServicio = models.AutoField(primary_key=True)
    fecha_informeServicio = models.DateField()
    adjunto_informeServicio = models.FileField(upload_to='informes_servicio/')
    revision = models.BooleanField()
    firma_area = models.BooleanField()
    firma_direccion = models.BooleanField()
    completo = models.BooleanField(default=False)
    nro_circuito = models.ForeignKey('Circuito', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"InformeServicio #{self.nro_informeServicio} - InformeArea #{self.nro_informeArea.nro_informeArea}"

class SolicitudInterarea(models.Model):
    nro_solicitudInterarea = models.AutoField(primary_key=True)
    fecha_solicitudInterarea = models.DateField()
    inter_areaTematica = models.CharField(choices=AREA_TEMATICA_CHOICES)
    muestras_solicitudIa = models.TextField()
    num_labs = models.IntegerField()
    observaciones = models.TextField(max_length=255, null=True)
    adjunto_solicitudInterarea = models.FileField(upload_to='solicitudes_interarea/')
    nro_circuito = models.ForeignKey('Circuito', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"SolicitudInterarea #{self.nro_solicitudInterarea} - InformeInterarea #{self.nro_informeInterarea.nro_informeInterarea}"

class DetalleInterarea(models.Model):
    nro_detalle = models.AutoField(primary_key=True)
    nro_solicitudInterarea = models.ForeignKey('SolicitudInterarea', on_delete=models.CASCADE)
    nro_servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE)

    def __str__(self):
        return f"DetalleInterarea #{self.nro_detalle} - SolicitudInterarea #{self.nro_solicitudInterarea.nro_solicitudInterarea} - Servicio #{self.nro_servicio.nro_servicio}"

class InformeInterarea(models.Model):
    nro_informeInterarea = models.AutoField(primary_key=True)
    fecha_informeInterarea = models.DateField()
    area_tematica = models.CharField(choices=AREA_TEMATICA_CHOICES)
    adjunto_informeInterarea = models.FileField(upload_to='informes_interarea/')
    nro_solicitudInterarea = models.ForeignKey('SolicitudInterarea', on_delete=models.CASCADE)
    nro_circuito = models.ForeignKey('Circuito', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"InformeInterarea #{self.nro_informeInterarea} - SolicitudInterarea #{self.nro_solicitudInterarea.nro_solicitudInterarea}"
    
class Circuito(models.Model):
    nro_circuito = models.AutoField(primary_key=True)
    finalizado = models.BooleanField(default=False)

class UltimoNumeroSingleton:
    _instance = None
    _ultimo_numero = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Inicializar el último número aquí, por ejemplo, con un valor predeterminado o recuperándolo de algún lugar.
            cls._nuevo_ultimo_numero = 0
        return cls._instance

    @property
    def ultimo_numero(self):
        return self._nuevo_ultimo_numero

    @ultimo_numero.setter
    def ultimo_numero(self, value):
        self._nuevo_ultimo_numero = value
