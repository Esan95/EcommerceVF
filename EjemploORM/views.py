#from inspect import ArgSpec
# from msilib.schema import Error
from sqlite3 import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from .models import Persona, Productos, productosComprados
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from .forms import ProductoForm

def inicio(request):
    sesion = None
    perfil = None
    ##Para evitar que se caiga al momento que la variable sea 0, para que no pase lo mismo ele GET en un formulario
    try:
        sesion = request.session['sesion_activa']
        perfil = request.session["sesion_perfil"]
        #perfil = request.session['sesion_perfil']
        if sesion != 'Activa':
            sesion = None
    except:
        sesion = None
        perfil = None
    return render(request,"index.html",{'sesion_activa':sesion,'sesion_perfil':perfil})
    

def respuesta(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request,"iniciar_sesion.html")
    return render(request,"respuesta.html",{'sesion_activa':sesion})

def listar(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request,"iniciar_sesion.html")
    p = Persona.objects.all()
    producto = Productos.objects.all()
    return render(request,"listar.html",{'sesion_activa':sesion, "personas":p, "productos":producto, 'sesion_perfil':request.session["sesion_perfil"]})

def listarEditar(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request,"iniciar_sesion.html")

    producto = Productos.objects.all()
    return render(request,"listarEditar.html",{'sesion_activa':sesion, "productos":producto})

def listarProductos(request):
    sesion = None
    producto = Productos.objects.filter(active=True)
    if producto:
            paginator = Paginator(producto, 9)
            page_number = request.GET.get('page')
            digital_products_data = paginator.get_page(page_number)
    
    try:
        sesion = request.session['sesion_activa']

    except:
        render(request,"listarProductos.html",{"productos":digital_products_data})

    return render(request,"listarProductos.html",{"productos":digital_products_data, 'sesion_activa':sesion})
    
def registro(request):
    msj = None
    rut_p = request.POST['rut']
    nombre_p = request.POST['nombre']
    direccion_p = request.POST['direccion']
    contrasenna_p = request.POST['contrasenna']
    correo_p = request.POST['email']
    telefono_p = request.POST['telefono']
    perfil_p = "usuario"

    enc_password = make_password(contrasenna_p)


    # Aqui se deben hacer las validaciones
    try:
        Persona.objects.create(rut=rut_p,nombre=nombre_p,direccion=direccion_p,
                                contrasenna = enc_password, correo_electronico = correo_p,
                                telefono = telefono_p, perfil=perfil_p)
        msj = 'se ha ingresado la persona'
    except Exception as ex:
        if str(ex.__cause__).find('EjemploORM_persona.rut') > 0:
            msj = 'ha ocurrido un problema en la operación, rut ya ingresado'
        elif str(ex.__cause__).find('EjemploORM_EjemploORM_persona.correo_electronico') > 0:
            msj = 'ha ocurrido un problema en la operación, correo electrónico ya ingresado'
        else:
            msj = 'ha ocurrido un problema en la operación'
    except Error as err:
        msj = f'ha ocurrido un problema en la operación_, {err}'

    return render(request,"respuesta.html",{'msj':msj})



def agregarProducto(request):
    data = {
        'form':ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data["msj"] = "Producto ingresado"
        else:
            data["form"] = formulario

    return render(request,"agregarProducto.html", data )

def ingresar(request):
    sesion = None
    perfil = None
    try:
        sesion = request.session['sesion_activa']
        perfil = request.session['sesion_perfil']
        return render(request,"ingresar.html",{'sesion_activa':sesion,'sesion_perfil':perfil})
    except:
        return render(request,"ingresar.html",{'sesion_activa':sesion,'sesion_perfil':perfil})

def ingresarProducto(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
        return render(request,"ingresarProducto.html",{'sesion_activa':sesion,'sesion_perfil':request.session["sesion_perfil"]})
    except:
        return render(request,"ingresarProducto.html",{'sesion_activa':sesion,'sesion_perfil':request.session["sesion_perfil"]})

def actualizar(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request,"iniciar_sesion.html")
    return render(request,"actualizar.html",{'sesion_activa':sesion,"form2":"hidden", 'sesion_perfil':request.session["sesion_perfil"]})

def actualiza(request):
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request,"iniciar_sesion.html")
    per = None
    msj = ""
    visibilidad =""
    try:
        per = Persona.objects.get(rut = request.GET["rut_busqueda"])
        visibilidad = "visible"
        return render(request, "actualizar.html", {"form2":visibilidad, "p":per,'sesion_activa':sesion})
    except:
        per = None
    
    if per == None:
        rut = None
        try:
            rut = request.POST["rut"]
        except:
            rut = None

        if rut != None:
            per = Persona.objects.get(rut = rut)
            nombre = request.POST["nombre"]
            direccion = request.POST["direccion"]
            correoElectronico = request.POST["email"]
            contrasenna = request.POST["contrasenna"]
            telefono = request.POST["telefono"]
            perfil = request.POST["perfil"]

            per.nombre = nombre
            per.direccion = direccion
            per.contrasenna = contrasenna
            per.correo_electronico = correoElectronico
            per.telefono = telefono
            per.perfil = perfil

            try:
                per.save()
                msj = "Se ha actualizado la persona"
            except:
                msj = "Se ha ocurrido un error al actualizar la persona"

            visibilidad = "hidden"
            return render(request, "actualizar.html", {"msj":msj, "form2":visibilidad,'sesion_activa':sesion,})
        
        else:
            msj = "No se ha encontrado la persona"
            visibilidad = "hidden"
            return render(request, "actualizar.html", {"msj":msj, "form2":visibilidad,'sesion_activa':sesion,})
    else:
        msj = "No se encontró la persona solicitada"
        visibilidad = "hidden"
        return render(request, "actualizar.html", {"msj":msj, "form2":visibilidad,'sesion_activa':sesion,})
            
    
def eliminar(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request,"iniciar_sesion.html",{'sesion_activa':sesion,'sesion_perfil':request.session["sesion_perfil"]})
    return render(request,"eliminar.html",{'sesion_activa':sesion, 'sesion_perfil':request.session["sesion_perfil"]})       

    
def elimina(request):
    msj = None
    try:
        per = Persona.objects.get(rut = request.GET["rut_busqueda"])
        per.delete()
        msj = "Persona eliminada"
        return render(request, "eliminar.html",{"msj":msj})
    except Exception as ex:
        if str(ex.args).find('does not exist') > 0:
            msj = 'Rut no existe'
        else:
            msj = 'Ha ocurrido un problema'
        
        return render(request,"eliminar.html", {"msj":msj})    

def iniciar_sesion(request):
    try:
        if request.session['sesion_activa'] == 'Activa':
            del request.session['sesion_activa']
            del request.session['sesion_perfil']
            return render(request,"iniciar_sesion.html")
        else:
            return render(request,"iniciar_sesion.html")
    except:
        return render(request, "iniciar_sesion.html")

def sesion(request):
    per = None
    try:
        per = Persona.objects.get(rut = request.POST["rut"])
        #if(per.contrasenna == request.POST["contrasenna"]):
        if(check_password(request.POST["contrasenna"], per.contrasenna)):
            request.session["sesion_activa"] = "Activa"
            request.session['sesion_nombre']=per.nombre
            request.session['sesion_perfil']=per.perfil
            return redirect(inicio)
        else:
            return render(request,"iniciar_sesion.html", {"mensaje":"contraseña no válida"})
    except Exception as ex:
        return render(request,"iniciar_sesion.html", {"mensaje":ex})

def modificarProducto(request, id):
    
    sesion = request.session['sesion_activa']

    producto = get_object_or_404 (Productos, id=id)
    
    data = {
        'form': ProductoForm(instance=producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="listarProductos")
        data["form"] = formulario
        data['sesion_activa'] = 'Activa'

    return render(request,"modificarProducto.html", data)

def eliminarProducto(request, id):
   
    producto = get_object_or_404 (Productos, id=id)
    producto.delete()

    return redirect(to="listarProductos")

def detalleProducto(request, id):
    sesion = None
    perfil = None
    try:
        sesion = request.session['sesion_activa']
        perfil = request.session['sesion_perfil']   
        producto = get_object_or_404 (Productos, id=id)

        return render(request,"detalleProducto.html",{ "producto":producto,'sesion_activa':sesion,'sesion_perfil':perfil})
    except:
        producto = get_object_or_404 (Productos, id=id)
        return render(request,"detalleProducto.html",{ "producto":producto,'sesion_activa':sesion,'sesion_perfil':perfil})
