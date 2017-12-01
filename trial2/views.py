# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,HttpResponse,render_to_response
from django.views.generic import TemplateView
from django.template import RequestContext
from trial2.forms import hform
import rdflib
from rdflib.plugins.sparql import prepareQuery
from geopy.geocoders import Nominatim
import openpyxl
import haversine
import ssl
# from django import template
#from myapp.models import PointOfInterest

g=rdflib.Graph()

g.parse("finale.rdf")



book = openpyxl.load_workbook("/home/karan/Downloads/trial.xlsx")
sheet = book.active
cells = sheet['A2':'D372']
di={}
dit={}
dit1={}


for c1, c2 ,c3,c4 in cells:
	di[c1.value]=c2.value 	# adrees, lat, lon
	dit[c1.value]=c3.value 	# address, resource
	dit1[c1.value]=c4.value  #address,primaryCategory
	#print ("adding address: " + c1.value)




# Create your views here.

class homeview(TemplateView):
	temp_name='index.html'
	def get(self,request,**kwargs):
		form=hform()	
		return render(request,self.temp_name,{'form':form})
	
	def post(self,request,**kwargs):
		ad = request.POST.get('address')
		#print("Temp first address",ad)

		def geocoding(ad):
				ad1=' '.join(ad.split(' ')[1:])
				print 'ad1',ad1
		#print("This is adress!",ad1)
				geolocator = Nominatim()
		# gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
				try:
					loc= geolocator.geocode(ad1)
				except GeocoderTimedOut:
					geocoding(ad1)
				print 'loc',loc
				if (loc):
					return loc
				else:
					geocoding(ad1)
		#print loc.address
		loc=geocoding(ad)
		k=[0] * 2
		k[0],k[1]=loc.latitude,loc.longitude
		#print "hey!",k 

		def gethaversine(src,dest):
			return haversine(src,dest,miles=True)
		
		# d=[]
		# for addr,pos in di.items():
		# 	po=str(pos).split(',')
		# 	#print addr,po
		# 	po=(float(po[0]),float(po[1]))
			
		# 	p=list(po)
		# 	#print addr,p
		# 	dist=haversine.haversine(k,p)
		# 	# for addr1,rn in dit.items():
		# 	if dist<10:
		# 		d.append([addr,format(dist, ".2f"),dit[addr]])
		# 		print addr,dit[addr]

		# d.sort(key =lambda x: x[1])

		# form=hform(request.POST)
		# form1=hform()
		if request.method != 'POST' :
			return render(request,self.temp_name,context=None)

		else:
			# if form.is_valid():
			#ToDo add primary Category	
				f1=f2=f3=f4=f5=f6=f7=f8=f9=f10=0
				text=request.POST.get('dd1')
				if text=='':
					raise ValidationError(_('Please select one value from list'))
				
				qu='http://example.org/data/resources#'+text
				ns='http://example.org/data/resources#'
				#ns1='https://doctorsinbloomington/resource/rdf'
				initNS = {'res':ns}

				if request.POST.getlist('ResourceName'):
					f1=1
					q = prepareQuery('SELECT ?rn  WHERE { ?a res:ResourceName ?rn . }',initNs=initNS)
					t=rdflib.URIRef(qu)
					for row in g.query(q, initBindings = {'a':t}):
							t1="%s" %row

				if request.POST.getlist('Addr'):
					f2=1
					q1 = prepareQuery('SELECT ?ad  WHERE { ?a res:Address_Line1 ?ad . }',initNs=initNS)
					t=rdflib.URIRef(qu)
					for row in g.query(q1, initBindings = {'a':t}):
							t2="%s" %row			

					q21 = prepareQuery('SELECT ?ad  WHERE { ?a res:City ?ad . }',initNs=initNS)
					t=rdflib.URIRef(qu)
					for row in g.query(q21, initBindings = {'a':t}):
							t3="%s" %row			  	

					q22 = prepareQuery('SELECT ?ad  WHERE { ?a res:State ?ad . }',initNs=initNS)
					t=rdflib.URIRef(qu)
					for row in g.query(q22, initBindings = {'a':t}):
							t4="%s" %row

					q23 = prepareQuery('SELECT ?ad  WHERE { ?a res:ZIP ?ad . }',initNs=initNS)
					t=rdflib.URIRef(qu)
					for row in g.query(q23, initBindings = {'a':t}):
							t5="%s" %row							




			  	if request.POST.getlist('Phone'):
					f6=1
					q1 = prepareQuery('SELECT ?pn  WHERE { ?a res:Phone ?pn . }',initNs=initNS)
					t=rdflib.URIRef(qu)
					for row in g.query(q1, initBindings = {'a':t}):
							t6="%s" %row

				if request.POST.getlist('description'):
					f7=1
					q2 = prepareQuery('SELECT ?des  WHERE { ?a res:Description ?des . }',initNs=initNS)
					t=rdflib.URIRef(qu)
					for row in g.query(q2, initBindings = {'a':t}):
							t7="%s" %row
				
				if request.POST.getlist('email'):
					f8=1
					q3 = prepareQuery('SELECT ?email  WHERE { ?a res:E_mail ?email . }',initNs=initNS)
					t=rdflib.URIRef(qu)
					for row in g.query(q3, initBindings = {'a':t}):
							t8="%s" %row 

				if request.POST.getlist('website'):
					f9=1
					q4 = prepareQuery('SELECT ?web  WHERE { ?a res:Website ?web . }',initNs=initNS)
					t=rdflib.URIRef(qu)
					for row in g.query(q4, initBindings = {'a':t}):
							t9 ="%s" %row

				rng=int(request.POST.get('ranged'))
					
				if rng == 2:
					d=[]
					for addr,pos in di.items():
						po=str(pos).split(',')
						#print addr,po
						po=(float(po[0]),float(po[1]))
						
						p=list(po)
						#print addr,p
						dist=haversine.haversine(k,p)
						# for addr1,rn in dit.items():
						if dist<2:
							d.append([addr,format(dist, ".2f"),dit[addr],dit1[addr]])
							#print addr,dit[addr]

					d.sort(key =lambda x: x[1])
					f10=1
					t10=d
				if rng == 5:
					d=[]
					for addr,pos in di.items():
						po=str(pos).split(',')
						#print addr,po
						po=(float(po[0]),float(po[1]))
						
						p=list(po)
						#print addr,p
						dist=haversine.haversine(k,p)
						# for addr1,rn in dit.items():
						if dist<5:
							d.append([addr,format(dist, ".2f"),dit[addr],dit1[addr]])
							#print addr,dit[addr]

					d.sort(key =lambda x: x[1])
					f10=1
					t10=d
				if rng == 10:
					d=[]
					for addr,pos in di.items():
						po=str(pos).split(',')
						#print addr,po
						po=(float(po[0]),float(po[1]))
						
						p=list(po)
						#print addr,p
						dist=haversine.haversine(k,p)
						# for addr1,rn in dit.items():
						if dist<10:
							d.append([addr,format(dist, ".2f"),dit[addr],dit1[addr]])
							#print addr,dit[addr]

					d.sort(key =lambda x: x[1])
					f10=1
					t10=d	


					
				
					
						



					#Todo get excel data for doctors and estimated cost
					#Todo Get excel data for disease and symptoms
					#Todo excel to rdf convertion
					#ToDO invisible symptoms
					#ToDO Error Handling
					#ToDO Front end

    			 	



				
				# ad = request.POST['location']
				# temp_ad = request.form['address']
				# temp_ad = form.cleaned_data['address']
				# print("first address",ad)
				# print("Temp first address",ad)
				# ad1=' '.join(ad.split(' ')[1:])
				# print("This is adress!",ad1)
				# geolocator = Nominatim()
				# loc= geolocator.geocode(ad1)
				#print loc.address
				# k=[0] * 2
				# k[0],k[1]=loc.latitude,loc.longitude 

				if (f1==1 and f2 ==0 and f6==0 and f7==0 and f8==0 and f9==0 and f10==1):
					args={'text':text,'t1':t1,'t10':t10,'k':k}
				if (f1==1 and f2==1 and f6 ==0 and f7==0 and f8==0 and f9==0 and f10==1 ):
					args={'text':text,'t1':t1,'t2':t2,'t10':t10,'k':k}
				if (f1==1 and f2==1 and f6==1 and f7 ==0 and f8==0 and f9==0 and f10==1):
					args={'text':text,'t1':t1,'t2':t2,'t3':t3,'t6':t6,'t10':t10,'k':k}
				if(f1==1 and f2==1 and f6==1 and f7==1 and f8==1 and f9==1 and f10==1):
					args={'text':text,'t1':t1,'t2':t2,'t3':t3,'t4':t4,'k':k,'t5':t5,'t6':t6,'t7':t7,'t8':t8,'t9':t9,'t10':t10}
						
				if(f1==1 and f2==1 and f9==1 and f7==1 and f8==0):
					args={'text':text,'t4':t4,'t2':t2,'t3':t3,'t5':t5,'t9':t9,'t7':t7,'k':k,'t10':t10}
				if(f1==1 and f2==0 and f7==1 and f9==1 and f8==0):
					args={'text':text,'t7':t7,'t9':t9,'k':k,'t10':t10,'t1':t1}
				if(f1==0 and f2==0 and f3==0 and f4==1):
					args={'text':text,'t4':t4,'k':k,'t10':t10}
				if(f1==0 and f2==1 and f3==0 and f4==0):
					args={'text':text,'t2':t2,'k':k,'t10':t10}
				if(f1==0 and f2==0 and f3==1 and f4==0):
					args={'text':text,'t3':t3,'k':k,'t10':t10}
				if(f1==1 and f9==1 and f8==0 and f7==0):
					args={'text':text,'t1':t1,'t2':t2,'t4':t4,'k':k,'t10':t10}
				if(f1==1 and f2==0 and f8==1 and f9==1):
					args={'text':text,'t1':t1,'t8':t8,'t9':t9,'k':k,'t10':t10}

				return render_to_response('index2.html', args)
			# else:
			# 	return render(request,'index.html',{'form1':form1})
	

	# def get_latlon(area):
		
	# 	geolocator = Nominatim()
	# 	loc= geolocator.geocode(area)
	# 	#print loc.address
	# 	k=[0] * 2
	# 	k[0],k[1]=loc.latitude,loc.longitude
	# 	return k
