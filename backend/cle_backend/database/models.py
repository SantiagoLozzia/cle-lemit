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

class Solicitante(models.Model):
    nro_solicitante = models.AutoField(primary_key=True)
    nombre_solicitante = models.CharField(max_length=255)
    cuit = models.CharField(max_length=20)
    pais = models.CharField(max_length=50)
    provincia = models.CharField(max_length=50)
    localidad = models.CharField(max_length=50)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    codigoPostal = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre_solic

class Presupuesto(models.Model):
    nro_presupuesto = models.AutoField(primary_key=True)
    fecha = models.DateField()
    contacto = models.CharField(max_length=255)
    email = models.EmailField()
    area_tematica = models.CharField(choices=AREA_TEMATICA_CHOICES)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.IntegerField(choices=DESCUENTO_CHOICES)
    arancel_presupuesto = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.TextField()
    estado_presupuesto = models.CharField(choices=ESTADO_PRESUPUESTO_CHOICES)
    nro_solicitante = models.ForeignKey('Solicitante', on_delete=models.PROTECT)

    def __str__(self):
        return f"Presupuesto #{self.nro_presupuesto} - Solicitante: {self.nro_solicitante.nombre_solic}, Área Temática: {self.get_area_tematica_display()}"

class Servicio(models.Model):
    nro_servicio = models.AutoField(primary_key=True)
    servicio = models.CharField(max_length=255)
    norma = models.CharField(max_length=255)
    arancel = models.IntegerField(validators=[MaxValueValidator(999999)])
    area_tematica = models.CharField(choices=AREA_TEMATICA_CHOICES)

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
    fecha = models.DateField()
    area_tematica = models.CharField(choices=AREA_TEMATICA_CHOICES)
    adjunto_solicitudServicio = models.FileField(upload_to='solicitudes_servicio/')
    contacto = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    obra = models.CharField(max_length=255)
    plazo_estimado = models.IntegerField() 
    cant_numLabs = models.IntegerField()
    muestras = models.TextField()
    observaciones = models.TextField()
    nro_presupuesto = models.ForeignKey('Presupuesto', on_delete=models.CASCADE)
    nro_legajo = models.ForeignKey('Legajo', on_delete=models.CASCADE)

    def __str__(self):
        return f"DataServicio #{self.nro_dataServicio} - Presupuesto #{self.nro_presupuesto.nro_presupuesto} - Legajo #{self.nro_legajo.nro_legajo}"

class Legajo(models.Model):
    nro_legajo = models.AutoField(primary_key=True)
    fecha = models.DateField()
    rangos_laboratorios = models.CharField(max_length=255)
    ultimo_numero = models.IntegerField(default=0)
    pago = models.BooleanField()
    plazo_pago = models.IntegerField(default=30)
    facturaAdjunta = models.BooleanField()
    adjunto_factura = models.FileField(upload_to='facturas/')
    nro_dataServicio = models.ForeignKey('DataServicio', on_delete=models.CASCADE)
    nro_ordenServicio = models.ForeignKey('OrdenServicio', on_delete=models.CASCADE)
    nro_recepcion = models.ForeignKey('Recepcion', on_delete=models.CASCADE)

    def __str__(self):
        return f"Legajo #{self.nro_legajo} - DataServicio #{self.nro_dataServicio.nro_dataServicio}"

    def actualizar_rangos_laboratorios(self, cant_numLabs):
        i = self.ultimo_numero + 1
        num_laboratorios = [str(i)]
        
        for _ in range(cant_numLabs - 1):
            i += 1
            num_laboratorios.append(str(i))
        
        self.ultimo_numero = i
        self.num_laboratorios = ', '.join(num_laboratorios)
        self.save()

class Recepcion(models.Model):
    nro_recepcion = models.AutoField(primary_key=True)
    nros_remitos = models.CharField(max_length=255)
    estado_recepcion = models.CharField(choices=ESTADO_RECEPCION_CHOICES)
    plazo_muestras = models.IntegerField(default=30)
    nro_legajo = models.OneToOneField('Legajo', on_delete=models.CASCADE)

    def __str__(self):
        return f"Recepcion #{self.nro_recepcion} - Legajo #{self.nro_legajo.nro_legajo}"

class OrdenServicio(models.Model):
    nro_ordenServicio = models.AutoField(primary_key=True)
    fecha = models.DateField()
    observaciones = models.TextField()
    nro_informeArea = models.ForeignKey('InformeArea', on_delete=models.CASCADE)  # Asegúrate de tener definida la clase InformeArea
    nro_legajo = models.ForeignKey('Legajo', on_delete=models.CASCADE)

    def __str__(self):
        return f"OrdenServicio #{self.nro_ordenServicio} - Legajo #{self.nro_legajo.nro_legajo}"

class InformeArea(models.Model):
    nro_informeArea = models.AutoField(primary_key=True)
    fecha = models.DateField()
    adjunto_informeServicio = models.FileField(upload_to='informes_areas/')
    nro_solicitud_interarea = models.ForeignKey('SolicitudInterarea', on_delete=models.CASCADE)  
    nro_informeServicio = models.ForeignKey('InformeServicio', on_delete=models.CASCADE)  
    nro_ordenServicio = models.ForeignKey('OrdenServicio', on_delete=models.CASCADE)

    def __str__(self):
        return f"InformeArea #{self.nro_informeArea} - OrdenServicio #{self.nro_ordenServicio.nro_ordenServicio}"
    
class InformeServicio(models.Model):
    nro_informeServicio = models.AutoField(primary_key=True)
    fecha = models.DateField()
    adjunto_informeServicio = models.FileField(upload_to='informes_servicio/')
    revision = models.BooleanField()
    firma_area = models.BooleanField()
    firma_direccion = models.BooleanField()
    nro_informeArea = models.ForeignKey('InformeArea', on_delete=models.CASCADE)

    def __str__(self):
        return f"InformeServicio #{self.nro_informeServicio} - InformeArea #{self.nro_informeArea.nro_informeArea}"

class SolicitudInterarea(models.Model):
    nro_solicitudInterarea = models.AutoField(primary_key=True)
    fecha = models.DateField()
    area_tematica = models.CharField(choices=AREA_TEMATICA_CHOICES)
    muestras_solicitudIa = models.TextField()
    num_labs = models.IntegerField()
    observaciones = models.TextField()
    adjunto_solicitudInterarea = models.FileField(upload_to='solicitudes_interarea/')
    nro_informeInterarea = models.ForeignKey('InformeInterarea', on_delete=models.CASCADE)  # Asegúrate de tener definida la clase InformeInterarea

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
    fecha = models.DateField()
    area_tematica = models.CharField(choices=AREA_TEMATICA_CHOICES)
    adjunto_informeInterarea = models.FileField(upload_to='informes_interarea/')
    nro_solicitudInterarea = models.ForeignKey('SolicitudInterarea', on_delete=models.CASCADE)

    def __str__(self):
        return f"InformeInterarea #{self.nro_informeInterarea} - SolicitudInterarea #{self.nro_solicitudInterarea.nro_solicitudInterarea}"