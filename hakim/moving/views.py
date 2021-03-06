from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from models import Meuble, CommandeParticulier, CommandeProfessionnel
from forms import MeubleQuantiteListForm, ParticulierContactForm, MeubleQuantiteFormSet, ProfessionnelContactForm
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils import simplejson
from decimal import Decimal
from django.core.urlresolvers import reverse

def particulier_devis(request):
    
    if request.method == 'POST':
        contact_form = ParticulierContactForm(request.POST)
        meublequantite_formset = MeubleQuantiteFormSet(request.POST)
        if contact_form.is_valid() and meublequantite_formset.is_valid(): 
            meubles = meublequantite_formset.save()
            commande = contact_form.save()
            for meuble in meubles:
                commande.meubles.add(meuble)
            commande.save()
            return render_to_response('moving/merci.html', {
                'commande': commande,
            }, context_instance=RequestContext(request))
    else:
        contact_form = ParticulierContactForm()
        meublequantite_formset = MeubleQuantiteListForm

    return render_to_response('moving/devis.html', {
        'contact_form': contact_form,
        'meublequantite_formset': meublequantite_formset
    }, context_instance=RequestContext(request))

def professionnel_devis(request):
    if request.method == 'POST':
        contact_form = ProfessionnelContactForm(request.POST)
#        meublequantite_formset = MeubleQuantiteFormSet(request.POST)
        if contact_form.is_valid():# and meublequantite_formset.is_valid(): 
#            meubles = meublequantite_formset.save()
            commande = contact_form.save()
#            for meuble in meubles:
#                commande.meubles.add(meuble)
            commande.save()
            return render_to_response('moving/merci.html', {
                'commande': commande,
            }, context_instance=RequestContext(request))
    else:
        contact_form = ProfessionnelContactForm()
#        meublequantite_formset = MeubleQuantiteListForm

    return render_to_response('moving/devis_professionnel.html', {
        'contact_form': contact_form,
#        'meublequantite_formset': meublequantite_formset
    }, context_instance=RequestContext(request))

def index(request):
    return render_to_response('moving/index.html', {
    }, context_instance=RequestContext(request))


@csrf_exempt
def calculate_volume(request):
    to_return = {
        'msg': u'No POST data sent.',
        'volume': None,
        }

    if request.method == "POST": # and is_ajax
        volume = Decimal(0)
        meublequantite_formset = MeubleQuantiteFormSet(request.POST)
        if meublequantite_formset.is_valid():
            dummy_commande = CommandeParticulier()
            for form in meublequantite_formset:
                volume = volume + Decimal(form.cleaned_data['quantite']) * form.cleaned_data['meuble'].volume
        to_return['volume'] = str(volume)
        to_return['msg'] = 'Success'

    data = simplejson.dumps(to_return)
    return HttpResponse(data, mimetype='application/json')