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

# import ssl



# Parsing the rdf file

g=rdflib.Graph() 
g.parse("finale.rdf")



#Load the excel file that has address,resource name,coordinates and primary category

book = openpyxl.load_workbook("/home/karan/Downloads/trial.xlsx")
sheet = book.active
cells = sheet['A2':'D372']
di={}
dit={}
dit1={}
# dit2={} #address and coordinates

#create the dictionary with following keys 
	# di-key=address, value=coordinates
	# dit-key=address,value=resource
	# dit1-key=address,value=primaryCategory

for c1, c2 ,c3,c4 in cells:
	di[c1.value]=c2.value 	# adrees, lat, lon
	dit[c1.value]=c3.value 	# address, resource
	dit1[c1.value]=c4.value  #address,primaryCategory
	


 

# Create your views here.
#My view to match the template

class homeview(TemplateView):
	temp_name='index.html'
	def get(self,request,**kwargs):
		form=hform()	
		return render(request,self.temp_name,{'form':form})
	
	def post(self,request,**kwargs):
		ad = request.POST.get('address')
		
		
#Geocoding to get the user coordinates with the user location
		def geocoding(ad):
			ad1=' '.join(ad.split(' ')[1:])
			# print 'ad1',ad1
			geolocator = Nominatim()
	
			try:
				loc= geolocator.geocode(ad1)
			# except GeocoderTimedOut:
			except:
				# geocoding(ad1)
				loc= geolocator.geocode(ad1)
			print 'loc',loc
			if (loc):
				return loc
			else:
				geocoding(ad1)
		
		

		#get the user coordinates after geocoding stored in the array k
		
		loc=geocoding(ad)
		k=[0] * 2
		k[0],k[1]=loc.latitude,loc.longitude
		 

		#validate if the request is not POST

		if request.method != 'POST' :
			return render(request,self.temp_name,context=None)

		else:
			# if form.is_valid():
				#variables to handle the dynamic request 
				f1=f2=f3=f4=f5=f6=f7=f8=f9=f10=0
				#text holds the input primary category 
				text=request.POST.get('dd1')
				#Input validation
				if text=='':
					raise ValidationError(_('Please select atleast one value from list'))
				

				#prepare the query after getting the user input

				qu='http://example.org/data/resources#'+text
				ns='http://example.org/data/resources#'
				
				#initialize the namespace

				initNS = {'res':ns}

				#If Resource name is requested, fire the prepared sparql query
				
				if request.POST.getlist('ResourceName'):
					f1=1
					q = prepareQuery('SELECT ?rn  WHERE { ?a res:ResourceName ?rn . }',initNs=initNS)
					t=rdflib.URIRef(qu)
					for row in g.query(q, initBindings = {'a':t}):
							t1="%s" %row

				#If Address is requested, fire the prepared sparql query

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


				#If Phone is requested, fire the prepared sparql query

				if request.POST.getlist('Phone'):
					f6=1
					q1 = prepareQuery('SELECT ?pn  WHERE { ?a res:Phone ?pn . }',initNs=initNS)
					t=rdflib.URIRef(qu)
					for row in g.query(q1, initBindings = {'a':t}):
							t6="%s" %row

				
				#If Description is requested, fire the prepared sparql query
				
				if request.POST.getlist('description'):
					f7=1
					q2 = prepareQuery('SELECT ?des  WHERE { ?a res:Description ?des . }',initNs=initNS)
					t=rdflib.URIRef(qu)
					for row in g.query(q2, initBindings = {'a':t}):
							t7="%s" %row
				
				
				#If email is requested, fire the prepared sparql query
				
				if request.POST.getlist('email'):
					f8=1
					q3 = prepareQuery('SELECT ?email  WHERE { ?a res:E_mail ?email . }',initNs=initNS)
					t=rdflib.URIRef(qu)
					for row in g.query(q3, initBindings = {'a':t}):
							t8="%s" %row 
				

				#If website is requested, fire the prepared sparql query

				if request.POST.getlist('website'):
					f9=1
					q4 = prepareQuery('SELECT ?web  WHERE { ?a res:Website ?web . }',initNs=initNS)
					t=rdflib.URIRef(qu)
					for row in g.query(q4, initBindings = {'a':t}):
							t9 ="%s" %row 

				
				#Get the range specified by the user 
				rng=int(request.POST.get('ranged'))
					
				#method to get the details of the resources near to the user by calculating the haversine distance
				def getDetails_Haversine(di,dit,dit1,rng):
					d=[]
					a=[]
					for addr,pos in di.items():
						po=str(pos).split(',')
						#print addr,po
						po=(float(po[0]),float(po[1]))
						
						p=list(po)
						#print addr,p
						dist=haversine.haversine(k,p)
						# for addr1,rn in dit.items():
						if dist<rng:
							d.append([addr,format(dist, ".2f"),dit[addr],dit1[addr]])
							a.append(list(po))

							#print addr,dit[addr]

					d.sort(key =lambda x: x[1])
					return d,a


				if rng == 2:
					d,a=getDetails_Haversine(di,dit,dit1,rng)
					f10=1
					t11=a
					#print 't11-->',t11
					t10=d
				if rng == 5:
					d,a=getDetails_Haversine(di,dit,dit1,rng)
					f10=1
					t10=d
					t11=a
				if rng == 10:
					d,a=getDetails_Haversine(di,dit,dit1,rng)
					f10=1
					t10=d
					t11=a	


					
				
					
						



					

    			 	



					#only resource name
				if (f1==1 and f2 ==0 and f6==0 and f7==0 and f8==0 and f9==0 and f10==1):
					args={'text':text,'t1':t1,'t10':t10,'k':k,'t11':t11}
					
					#only resource name and address
				if (f1==1 and f2==1 and f6 ==0 and f7==0 and f8==0 and f9==0 and f10==1 ):
					args={'text':text,'t1':t1,'t2':t2,'t3':t3,'t4':t4,'t5':t5,'t10':t10,'k':k,'t11':t11}
					
					#resource name,address and Phone
				if (f1==1 and f2==1 and f6==1 and f7 ==0 and f8==0 and f9==0 and f10==1):
					args={'text':text,'t1':t1,'t2':t2,'t3':t3,'t4':t4,'t5':t5,'t6':t6,'t10':t10,'k':k,'t11':t11}

				if (f1==1 and f2==1 and f6==1 and f7 ==1 and f8==0 and f9==0 and f10==1):
					args={'text':text,'t1':t1,'t2':t2,'t3':t3,'t4':t4,'t5':t5,'t6':t6,'t10':t10,'k':k,'t11':t11,'t7':t7}	

					#resource name,address,phone and email
				if (f1==1 and f2==1 and f6==1 and f7 ==0 and f8==1 and f9==0 and f10==1):
					args={'text':text,'t1':t1,'t2':t2,'t3':t3,'t4':t4,'t5':t5,'t6':t6,'t10':t10,'k':k,'t11':t11,'t8':t8}
				
					#All
				if(f1==1 and f2==1 and f6==1 and f7==1 and f8==1 and f9==1 and f10==1):
					args={'text':text,'t1':t1,'t2':t2,'t3':t3,'t4':t4,'k':k,'t5':t5,'t6':t6,'t7':t7,'t8':t8,'t9':t9,'t10':t10,'t11':t11}
				
					#resource name and phone
				if (f1==1 and f2==0 and f6 ==1 and f7==0 and f8==0 and f9==0 and f10==1 ):
					args={'text':text,'t1':t1,'t6':t6,'t10':t10,'k':k,'t11':t11}
					
					#resource name,description
				if (f1==1 and f2==0 and f6 ==0 and f7==1 and f8==0 and f9==0 and f10==1 ):
					args={'text':text,'t1':t1,'t7':t7,'t10':t10,'k':k,'t11':t11}
				
					#resource name and email
				if (f1==1 and f2==0 and f6 ==0 and f7==0 and f8==1 and f9==0 and f10==1 ):
					args={'text':text,'t1':t1,'t8':t8,'t10':t10,'k':k,'t11':t11}
						
					#resource name,address,website,description
				if(f1==1 and f2==1 and f9==1 and f7==1 and f8==0):
					args={'text':text,'t1':t1,'t4':t4,'t2':t2,'t3':t3,'t5':t5,'t9':t9,'t7':t7,'k':k,'t10':t10,'t11':t11}
					
					#resource name,description,website
				if(f1==1 and f2==0 and f7==1 and f9==1 and f8==0):
					args={'text':text,'t7':t7,'t9':t9,'k':k,'t10':t10,'t1':t1,'t11':t11}
				
					#resource name and website
				if(f1==1 and f2==0 and f7==0 and f8==0 and f9==1):
					args={'text':text,'t1':t1,'t9':t9,'k':k,'t10':t10,'t11':t11}
					#resource name,address and website
				if(f1==1 and f2==1 and f7==0 and f8==0 and f9==1):
					args={'text':text,'t1':t1,'t2':t2,'t3':t3,'t4':t4,'t5':t5,'t9':t9,'k':k,'t10':t10,'t11':t11}

				if(f1==1 and f2==1 and f7==0 and f8==1 and f9==0):
					args={'text':text,'t1':t1,'t2':t2,'t3':t3,'t4':t4,'t5':t5,'t8':t8,'k':k,'t10':t10,'t11':t11}	
					
					#resource name description , email and website
				if(f1==1 and f2==0 and f7==1 and f8==1 and f9==1):
					args={'text':text,'t7':t7,'t8':t8,'k':k,'t10':t10,'t11':t11,'t9':t9}

					#resource name,address description , email and website

				if(f1==1 and f2==1 and f7==1 and f8==1 and f9==1 and f6==0):
					args={'text':text,'t7':t7,'t8':t8,'k':k,'t10':t10,'t11':t11,'t9':t9,'t1':t1,'t2':t2,'t3':t3,'t4':t4,'t5':t5}	
				
				if(f1==0 and f2==0 and f6==1 and f7==0):
					args={'text':text,'t6':t6,'k':k,'t10':t10,'t11':t11,'t7':t7}
				if(f1==1 and f9==1 and f8==0 and f7==0 and f2==0):
					args={'text':text,'t1':t1,'t9':t9,'k':k,'t10':t10,'t11':t11}
				if(f1==1 and f2==0 and f8==1 and f9==1 and f7==0 and f2==0):
					args={'text':text,'t1':t1,'t8':t8,'t9':t9,'k':k,'t10':t10,'t11':t11}

				

				return render_to_response('index2.html', args)
			