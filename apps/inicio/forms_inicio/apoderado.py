from datetimewidget.widgets import DateWidget
from django import forms

from apps.inicio.forms_inicio.persona import PersonaForm
from ..models import Apoderado, PersonaSexos, Persona, Estudiante


class SearchField(forms.TextInput):
    template_name = 'campos/search.html'


class ApoderadoForm(forms.ModelForm):
    personaid = forms.IntegerField(
        initial=-1,
        widget=forms.HiddenInput()
    )

    dni = forms.CharField(
        label='DNI Apoderado',
        widget=SearchField(attrs={'placeholder': 'DNI Apoderado'}),
        min_length=8,
        max_length=8
    )

    paterno = forms.CharField(
        label='Apellido Paterno',
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese apellido paterno'})
    )

    materno = forms.CharField(
        label='Apellido Materno',
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese apellido materno'})
    )

    nombre = forms.CharField(
        label='Nombre',
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese nombre'})
    )

    sexo = forms.ChoiceField(
        choices=PersonaSexos
    )

    fechanacimiento = forms.DateField(
        label='Fecha de nacimiento',
        input_formats=["%d/%m/%Y"],
        widget=DateWidget(
            attrs={"data-datepicker-type": "4", "data-provider": "datepicker-inline"},
            bootstrap_version=3,
            options={
                "format": "dd/mm/yyyy",
                # "startView": "2",
                "autoclose": "true",
                "language": "es",
                "fontAwesome": "true",
                # "todayBtn": "true",
                "clearBtn": "false"
            }
        )
    )

    telefono = forms.CharField(
        label='Telefono',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Telefono'
        })
    )

    celular = forms.CharField(
        label='Celular',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Celular',
        }),
        min_length=9,
        max_length=9
    )

    correo = forms.CharField(
        label='Correo',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Correo',
        })
    )

    direccion = forms.CharField(
        label='Direccion',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Direccion',
        })
    )

    ocupacion = forms.CharField(
        label='Ocupacion del Apoderado',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ocupacion'
        })
    )

    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs.pop('kwargs')
        super(ApoderadoForm, self).__init__(*args, **kwargs)

        _apoderado = None
        try:
            if self.kwargs['pk']:
                _apoderado = Apoderado.objects.get(id=Estudiante.objects.get(id=self.kwargs['pk']).apoderado_id)
        except Apoderado.DoesNotExist:
            _apoderado = None
        except Exception as e:
            print(str(e.message))

        if not _apoderado == None:
            self.fields['personaid'].initial = _apoderado.persona_id
            self.fields['dni'].initial = _apoderado.persona.dni
            self.fields['paterno'].initial = _apoderado.persona.paterno
            self.fields['materno'].initial = _apoderado.persona.materno
            self.fields['nombre'].initial = _apoderado.persona.nombre
            self.fields['sexo'].initial = _apoderado.persona.sexo
            self.fields['fechanacimiento'].initial = _apoderado.persona.fechanacimiento
            self.fields['telefono'].initial = _apoderado.persona.telefono
            self.fields['celular'].initial = _apoderado.persona.celular
            self.fields['correo'].initial = _apoderado.persona.correo
            self.fields['direccion'].initial = _apoderado.persona.direccion
            self.fields['ocupacion'].initial = _apoderado.ocupacion

        self.fields['celular'].widget.attrs['attr'] = "number"
        for i, (fname, field) in enumerate(self.fields.iteritems()):
            field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'

    class Meta:
        model = Apoderado
        fields = [
            'ocupacion'
        ]

    # Validar los formularios
    def clean(self):
        apoderado = super(ApoderadoForm, self).clean()
        persona = Persona.objects.filter(
            dni=apoderado['dni']
        ).exclude(
            id=apoderado['personaid']
        )

        if persona.count() > 0:
            self.add_error('Ya existe una persona registrada con este DNI')

        if self.instance.pk == None:
            estudiante = Estudiante.objects.get(pk=self.kwargs.get('estudiante'))
            if estudiante.persona.dni == apoderado['dni']:
                self.add_error('dni', 'EL dni del Apoderado no puede ser igual al dni del Estudiante')

    def save(self, commit=False):
        estudiante = None
        try:
            if not self.kwargs.get('estudiante') == None:
                estudiante = Estudiante.objects.get(pk=self.kwargs.get('estudiante'))
            else:
                estudiante = Estudiante.objects.get(pk=self.kwargs.get('pk'))
        except Estudiante.DoesNotExist:
            estudiante = None
        except Exception as e:
            print(str(e.message))

        apoderado = super(ApoderadoForm, self).save(commit=False)
        data = self.cleaned_data

        if data.get('personaid') == 0:
            persona = PersonaForm(data)
            persona.save()

            apo = Apoderado(persona=Persona.objects.get(dni=data.get('dni')), ocupacion=data.get('ocupacion'))
            apo.save()

            # Actualizar el apoderdo del estudiante de la fila seleccionada
            estudiante.apoderado = apo
            estudiante.save()
        else:
            objPersona = Persona.objects.get(pk=data.get('personaid'))
            persona = PersonaForm(data, instance=objPersona)
            persona.save()

            try:
                objApoderado = Apoderado.objects.get(persona_id=data.get('personaid'))
            except Apoderado.DoesNotExist:
                objApoderado = None

            if objApoderado == None:
                apo = Apoderado(persona=Persona.objects.get(dni=data.get('dni')), ocupacion=data.get('ocupacion'))
                apo.save()

                estudiante.apoderado = apo
                estudiante.save()
            else:
                objApoderado.ocupacion = data.get('ocupacion')
                objApoderado.save()

                estudiante.apoderado = objApoderado
                estudiante.save()
        return apoderado
