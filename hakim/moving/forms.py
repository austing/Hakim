#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.forms import ModelForm, Form
from django.forms.models import modelform_factory, BaseModelFormSet
from django.forms.widgets import HiddenInput, TextInput
from django.contrib.admin.widgets import AdminDateWidget
from models import CommandeParticulier, MeubleQuantite, Meuble
from django.utils.safestring import mark_safe
from django.forms.formsets import BaseFormSet, formset_factory
from models import Chambre


class SpinnerWidget(TextInput):
    def __init__(self, *args, **kwargs):
        super(SpinnerWidget, self).__init__(*args, **kwargs)
        if 'class' in self.attrs:
            self.attrs['class'] += ' spinner'
        else:
            self.attrs['class'] = ' spinner'
#    class Media:
#        js = ('js/spinner.js',) #'jquery-ui-1.9.2.custom/js/jquery-1.8.3.js', 'jquery-ui-1.9.2.custom/js/jquery-ui-1.9.2.custom.min.js', 

class ParticulierContactForm(ModelForm):
    class Meta:
        model = CommandeParticulier
        exclude = ('etat_de_commande','destination_addresse','origine_addresse','meubles')
    def __init__(self, *args, **kwargs):
        super(ParticulierContactForm, self).__init__(*args, **kwargs)
        self.fields['date_chargement'].widget = AdminDateWidget()
        self.fields['date_dechargement'].widget = AdminDateWidget()
        self.fields['origine_etages_sans_ascenseur'].widget = SpinnerWidget();
        self.fields['destination_etages_sans_ascenseur'].widget = SpinnerWidget();


initial_meublequantite = []
for meuble in Meuble.objects.all().order_by('chambre'):
    initial_meublequantite.append({'meuble':meuble.id,'quantite':0})

class MeubleHiddenInput(HiddenInput):
    def __init__(self, *args, **kwargs):
        self.special_label=kwargs.pop('special_label',None)
        super(MeubleHiddenInput, self).__init__(*args, **kwargs)
    def render(self, *args, **kwargs):
        print "." # Unless I print something here, the form doesn't appear.
        value = args[1]
        try:
            meuble = Meuble.objects.get(pk=value)
        except:
            meuble = None
        old_render = super(MeubleHiddenInput, self).render(*args,**kwargs)
        if meuble:
            output = mark_safe("<span class=\"labelled-hidden-input-text\">" + old_render + ' ' + meuble.nom_pluriel + "</span>")
            return output
        else: # invalid meuble
            return "meuble non-existent"
# static/js/jquery-ui-1.9.2.custom/css/ui-darkness/jquery-ui-1.9.2.custom.min.css
# static/jquery-ui-1.9.2.custom/js/jquery-1.8.3.js
# static/jquery-ui-1.9.2.custom/js/jquery-ui-1.9.2.custom.min.js



class MeublesSpinnerWidget(TextInput):
    def __init__(self, *args, **kwargs):
        super(MeublesSpinnerWidget, self).__init__(*args, **kwargs)
        if 'class' in self.attrs:
            self.attrs['class'] += ' meuble-quantite spinner'
        else:
            self.attrs['class'] = ' meuble-quantite spinner'
    class Media:
        js = ('js/meubles.js',) #'jquery-ui-1.9.2.custom/js/jquery-1.8.3.js', 'jquery-ui-1.9.2.custom/js/jquery-ui-1.9.2.custom.min.js', 

class MeubleQuantiteForm(ModelForm):
    error_css_class = "error"
    class Meta:
        model = MeubleQuantite
    def __init__(self, *args, **kwargs):
        print '.' # otherwise it doesn't recognize the models that should be included!
        super(MeubleQuantiteForm, self).__init__(*args, **kwargs)

        self.chambre = None
        if 'meuble' in self.initial and self.initial['meuble']:
            self.chambre = Meuble.objects.get(pk=self.initial['meuble']).chambre
        else:
            key = self.prefix+'-meuble'
            if key in self.data and self.data[key]:
                self.chambre = Meuble.objects.get(pk=self.data[key]).chambre

        self.fields['quantite'].widget = MeublesSpinnerWidget()
        self.fields['meuble'].widget = MeubleHiddenInput()

class MeubleFormSet(BaseModelFormSet):
    error_css_class = "error"
    def __init__(self, *args, **kwargs):
        super(MeubleFormSet, self).__init__(*args, **kwargs)
        self.chambres = Chambre.objects.all()
    def as_ul(self):
        current_chambre = None
        render = '<ul class="chambres">'
        for form in self:
            chambre = form.chambre
            if chambre and chambre.id != current_chambre:
                if current_chambre:
                    render = render + "</ul></li>"
                render = render + u"<li class=\"chambre\"><span class='toggle-triangle'>▼</span> <a class='togglelink'>%s</a></li><ul class='meubles'>" % chambre.nom.title()
                current_chambre = chambre.id
            render = render + form.as_ul()
        if current_chambre:
            render = render + "</ul>"
        render = render + "</ul>"
        return mark_safe(u'\n'.join([unicode(self.management_form), render]))

def meuble_formset_factory(form, formset=MeubleFormSet, extra=1, can_order=False,
                    can_delete=False, max_num=None):
    attrs = {'form': form, 'extra': extra,
             'can_order': can_order, 'can_delete': can_delete,
             'max_num': max_num}
    return type(form.__name__ + 'FormSet', (formset,), attrs)

def meuble_modelformset_factory(model, form=ModelForm, formfield_callback=None,
                         formset=MeubleFormSet,
                         extra=1, can_delete=False, can_order=False,
                         max_num=None, fields=None, exclude=None):
    form = modelform_factory(model, form=form, fields=fields, exclude=exclude,
                             formfield_callback=formfield_callback)
    FormSet = meuble_formset_factory(form, formset, extra=extra, max_num=max_num,
                              can_order=can_order, can_delete=can_delete)
    FormSet.model = model
    return FormSet

MeubleQuantiteFormSet = meuble_modelformset_factory(MeubleQuantite,form=MeubleQuantiteForm,extra=len(initial_meublequantite))

MeubleQuantiteListForm = MeubleQuantiteFormSet(queryset=MeubleQuantite.objects.none(), initial=initial_meublequantite)
