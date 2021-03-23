from django.shortcuts import render
from .models import general_m

# Create your views here.

def general(request):
    data=general_m.objects.all()

    return render(request,"base.html")


def general1(request):
    print('form submited!')
    
   # this is to send data to db
    slabs = int(request.POST.get('slabs'))
    length=int(request.POST.get('length'))
    breadth=int(request.POST.get('breadth'))
    height=int(request.POST.get('height'))
    cost=int(request.POST.get('cost'))
    nodes=int(request.POST.get('nodes'))
    
    print(slabs)
    

    result=[]
    def opti(slabs,length,breadth,height,cost,nodes):
        import math

        dist_from_base_center=[]
        dist_from_base_refnode=[]

        def distance(x, y, z):
            Euclidean_dist=(x**2+y**2+z**2)**0.5
            dist_from_base_center.append(Euclidean_dist)
            return Euclidean_dist

        def distance1(x1, y1, z1):
            Euclidean_dist1=((x1)**2+(y1)**2+(z1)**2)**0.5
            dist_from_base_refnode.append(Euclidean_dist1)
            return Euclidean_dist1

        def simp_converter(accesible_coordinates_center,accesible_coordinates_refnode,a,b,c):  
            #accesible_coordinates_center=[(1,-1,0),(0,-1,0),(-1,-1,0),(-1,0,0),(-1,1,0),(0,1,0),(1,1,0),(1,-1,1),(0,-1,1),(-1,-1,1),(-1,0,1),(0,0,1),(1,0,1),(1,1,1),(0,1,1),(-1,1,1)]
            accesible_coordinates_center_actual=[]
            
            for input1 in accesible_coordinates_center:
                x = input1[0]*a
                y = input1[1]*b
                z = input1[2]*c
                tup = (x, y, z)
                accesible_coordinates_center_actual.append(tup)

            #accesible_coordinates_refnode=[(0,-1,0),(-2,0,0),(0,1,0),(-1,-1,0),(-1,1,0),(-2,-1,0),(-2,1,0),(0,-1,1),(-2,0,1),(0,1,1),(-1,-1,1),(-1,0,1),(-1,1,1),(-2,-1,1),(0,0,1),(-2,1,1)]
            accesible_coordinates_refnode_actual=[]
            for input2 in accesible_coordinates_refnode:
                x1 = input2[0]*a
                y1 = input2[1]*b 
                z1 = input2[2]*c
                tup1 = (x1, y1, z1)
                accesible_coordinates_refnode_actual.append(tup1)
            #print('-------------------------------------------------------------------------------------------')
            #print('----> center: \n',accesible_coordinates_center_actual)
            #print('----> center: \n',len(accesible_coordinates_center_actual))
            #print('-------------------------------------------------------------------------------------------')
            #print('ref \n',accesible_coordinates_refnode_actual)
            #print('ref \n',len(accesible_coordinates_refnode_actual))
            #print('-------------------------------------------------------------------------------------------')
            return(accesible_coordinates_center_actual,accesible_coordinates_refnode_actual)

        def center_coord_genrator(n):
            #n=int(input('input no of slabs on x-axis(even no. only): '))
            y=int(-1*(n/2))
            y1=int(n/2)
            accesible_coordinates_center=[]
            for i in range(y,y1+1):
                for j in range(int(-1),2):
                    for k in range(0,2):
                        tup= (i,j,k)
                        if (tup==(0,0,0) or tup==(i,0,0)):
                            if (tup == (y,0,0)):
                                xyz=1
                                xyz+=1
                                #accesible_coordinates_center.append(tup)
                            
                        else :
                            accesible_coordinates_center.append(tup)
        


            #print('accesible coordinates center: \n',accesible_coordinates_center)
            #print('accesible_coordinates_center: ',len(accesible_coordinates_center))
            return(accesible_coordinates_center)

        def refnode_coord_genrator(n):
            #n=int(input('input no of slabs on x-axis(even no. only): '))
            
            accesible_coordinates_refnode=[]
            for i in range(0,n+1):
                for j in range(int(-1),2):
                    for k in range(0,2):
                        tup= (i,j,k)
                        if (tup==(0,0,0) or tup==(i,0,0)):
                            if (tup == (n,0,0)):
                                xyz=1
                                xyz+=1
                                #accesible_coordinates_refnode.append(tup)
                            
                        else :
                            accesible_coordinates_refnode.append(tup)

            
            #print('accesible coordinates center: \n',accesible_coordinates_refnode)
            #print('accesible_coordinates_center: ',len(accesible_coordinates_refnode))
            return(accesible_coordinates_refnode)



        n=slabs#int(input('input no of slabs on x-axis(even no. only): '))
        a=length#(float(input('total length of container: '))/n)
        b=breadth#(float(input('total breadth of container: '))/2)
        c=height#(float(input('total height of container: '))/2)
        accesible_coordinates_center=center_coord_genrator(n)
        accesible_coordinates_refnode=refnode_coord_genrator(n)

        output=simp_converter(accesible_coordinates_center,accesible_coordinates_refnode,a,b,c)

        accesible_coordinates_center=output[0]
        #print(accesible_coordinates_center)
        num=len(accesible_coordinates_center)

        for input1 in accesible_coordinates_center:
            x = input1[0]
            y = input1[1] 
            z = input1[2]
            distance(x, y, z)

        accesible_coordinates_refnode=output[1]
        #print(accesible_coordinates_refnode)
        for input2 in accesible_coordinates_refnode:
            x1 = input2[0]
            y1 = input2[1] 
            z1 = input2[2]
            distance1(x1, y1, z1)

        def optimizer1(C,N):
            from gekko import GEKKO as gk 
            import math
            
            nlp = gk(remote=False)

            nlp.options.SOLVER=1  # APOPT is an MINLP solver


            # defining variables

            x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15 = nlp.Array(nlp.Var,15,lb=0,ub=1,integer=True)

            a1=dist_from_base_center[0]
            a2=dist_from_base_center[1]
            a3=dist_from_base_center[2]
            a4=dist_from_base_center[3]
            a5=dist_from_base_center[4]
            a6=dist_from_base_center[5]
            a7=dist_from_base_center[6]
            a8=dist_from_base_center[7]
            a9=dist_from_base_center[8]
            a10=dist_from_base_center[9]
            a11=dist_from_base_center[10]
            a12=dist_from_base_center[11]
            a13=dist_from_base_center[12]
            a14=dist_from_base_center[13]
            a15=dist_from_base_center[14]


            #incentive coeff for objective function
            d1= dist_from_base_refnode[0]
            d2= dist_from_base_refnode[1]
            d3= dist_from_base_refnode[2]
            d4= dist_from_base_refnode[3]
            d5= dist_from_base_refnode[4]
            d6= dist_from_base_refnode[5]
            d7= dist_from_base_refnode[6]
            d8= dist_from_base_refnode[7]
            d9= dist_from_base_refnode[8]
            d10= dist_from_base_refnode[9]
            d11= dist_from_base_refnode[10]
            d12= dist_from_base_refnode[11]
            d13= dist_from_base_refnode[12]
            d14= dist_from_base_refnode[13]
            d15= dist_from_base_refnode[14]

        
        
            d0 = 0.99

            n = 3.61

            z=10*n*nlp.log(d1/d0)*x1*a1 + 10*n*nlp.log(d2/d0)*x2*a2 + 10*n*nlp.log(d3/d0)*x3*a3+10*n*nlp.log(d4/d0)*x4*a4+10*n*nlp.log(d5/d0)*x5*a5+10*n*nlp.log(d6/d0)*x6*a6+10*n*nlp.log(d7/d0)*x7*a7 + 10*n*nlp.log(d8/d0)*x8*a8 + 10*n*nlp.log(d9/d0)*x9*a9 + 10*n*nlp.log(d10/d0)*x10*a10 + 10*n*nlp.log(d11/d0)*x11*a11 + 10*n*nlp.log(d12/d0)*x12*a12 + 10*n*nlp.log(d13/d0)*x13*a13 + 10*n*nlp.log(d14/d0)*x14*a14 +10*n*nlp.log(d15/d0)*x15*a15 
            # constraint equation.
        
            nlp.Equation(x1+x2+x3+x4+x5+x6+x7+x8+x9+x10+x11+x12+x13+x14+x15 ==N)
            nlp.Equation(1722*(x1+x2+x3+x4+x5+x6+x7+x8+x9+x10+x11+x12+x13+x14+x15) <= C)
            nlp.Minimize(z)
            nlp.solve(disp=False)
            
            #print('x1:'+ str(x1.value[0]))
            result.append('x1:'+ str(x1.value[0]))
            result.append('x2:'+ str(x2.value[0]))
            result.append('x3:'+ str(x3.value[0]))
            result.append('x4:'+ str(x4.value[0]))
            result.append('x5:'+ str(x5.value[0]))
            result.append('x6:'+ str(x6.value[0]))
            result.append('x7:'+ str(x7.value[0]))
            result.append('x8:'+ str(x8.value[0]))
            result.append('x9:'+ str(x9.value[0]))
            result.append('x10:'+ str(x10.value[0]))
            result.append('x11:'+ str(x11.value[0]))
            result.append('x12:'+ str(x12.value[0]))
            result.append('x13:'+ str(x13.value[0]))
            result.append('x14:'+ str(x14.value[0]))
            result.append('x15:'+ str(x15.value[0]))
            
            #result.append('Objective:' + str(nlp.options.objfcnval))
            #print('d3 :',d12,'a3 :', a12)
            #print('d4 :',d15,'a4 :', a15)
            

        def optimizer2(C,N): 
            from gekko import GEKKO as gk
            import math
            nlp = gk(remote=False)

            nlp.options.SOLVER=1  # APOPT is an MINLP solver


            # defining variables

            x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16,x17,x18,x19,x20,x21,x22,x23,x24,x25 = nlp.Array(nlp.Var,25,lb=0,ub=1,integer=True)
            #x_list=[]
            #a_list=[]
            #d_list=[]
            
            # for i in range(1,num+1):
            #  x_list.append('x'+str(i))
            #for i in range(1,num+1):
            #   a_list.append('x'+str(i))
            #for i in range(1,num+1):
            #   d_list.append('x'+str(i))

            #for l in x_list:
            #   l = nlp.Array(nlp.Var,1,lb=0,ub=1,integer=True)
            #   print(l)
            #o=0
            #for m in a_list:
            #  m = dist_from_base_center[o]
            #  o += 1
            #  print(m)

            d1=dist_from_base_refnode[0]
            d2=dist_from_base_refnode[1]
            d3=dist_from_base_refnode[2]
            d4=dist_from_base_refnode[3]
            d5=dist_from_base_refnode[4]
            d6=dist_from_base_refnode[5]
            d7=dist_from_base_refnode[6]
            d8=dist_from_base_refnode[7]
            d9=dist_from_base_refnode[8]
            d10=dist_from_base_refnode[9]
            d11=dist_from_base_refnode[10]
            d12=dist_from_base_refnode[11]
            d13=dist_from_base_refnode[12]
            d14=dist_from_base_refnode[13]
            d15=dist_from_base_refnode[14]
            d16=dist_from_base_refnode[15]
            d17=dist_from_base_refnode[16]
            d18=dist_from_base_refnode[17]
            d19=dist_from_base_refnode[18]
            d20=dist_from_base_refnode[19]
            d21=dist_from_base_refnode[20]
            d22=dist_from_base_refnode[21]
            d23=dist_from_base_refnode[22]
            d24=dist_from_base_refnode[23]
            d25=dist_from_base_refnode[24]

            
            
            #incentive coeff for objective function
            a1=dist_from_base_center[0]
            a2=dist_from_base_center[1]
            a3=dist_from_base_center[2]
            a4=dist_from_base_center[3]
            a5=dist_from_base_center[4]
            a6=dist_from_base_center[5]
            a7=dist_from_base_center[6]
            a8=dist_from_base_center[7]
            a9=dist_from_base_center[8]
            a10=dist_from_base_center[9]
            a11=dist_from_base_center[10]
            a12=dist_from_base_center[11]
            a13=dist_from_base_center[12]
            a14=dist_from_base_center[13]
            a15=dist_from_base_center[14]
            a16=dist_from_base_center[15]
            a17=dist_from_base_center[16]
            a18=dist_from_base_center[17]
            a19=dist_from_base_center[18]
            a20=dist_from_base_center[19]
            a21=dist_from_base_center[20]
            a22=dist_from_base_center[21]
            a23=dist_from_base_center[22]
            a24=dist_from_base_center[23]
            a25=dist_from_base_center[24]



            
            #p=0
            #for n in d_list:
            # n = dist_from_base_refnode[p]
            # p += 1
                #print(n)    
        
            d0 = 0.99

            n = 3.61

            z=10*n*nlp.log(d1/d0)*x1*a1 + 10*n*nlp.log(d2/d0)*x2*a2 + 10*n*nlp.log(d3/d0)*x3*a3+10*n*nlp.log(d4/d0)*x4*a4+10*n*nlp.log(d5/d0)*x5*a5+10*n*nlp.log(d6/d0)*x6*a6+10*n*nlp.log(d7/d0)*x7*a7 + 10*n*nlp.log(d8/d0)*x8*a8 + 10*n*nlp.log(d9/d0)*x9*a9 + 10*n*nlp.log(d10/d0)*x10*a10 +10*n*nlp.log(d11/d0)*x11*a11 + 10*n*nlp.log(d12/d0)*x12*a12 + 10*n*nlp.log(d13/d0)*x13*a13+10*n*nlp.log(d14/d0)*x14*a14+10*n*nlp.log(d15/d0)*x15*a15+10*n*nlp.log(d16/d0)*x16*a16+10*n*nlp.log(d17/d0)*x17*a17 + 10*n*nlp.log(d18/d0)*x18*a18 + 10*n*nlp.log(d19/d0)*x19*a19 + 10*n*nlp.log(d20/d0)*x20*a20+10*n*nlp.log(d21/d0)*x21*a21 + 10*n*nlp.log(d22/d0)*x22*a22 + 10*n*nlp.log(d23/d0)*x23*a23+10*n*nlp.log(d24/d0)*x24*a24+10*n*nlp.log(d25/d0)*x25*a25   # constraint equation.
        
            nlp.Equation(x1+x2+x3+x4+x5+x6+x7+x8+x9+x10+x11+x12+x13+x14+x15+x16+x17+x18+x19+x20+x21+x22+x23+x24+x25 ==N)
            nlp.Equation(1722*(x1+x2+x3+x4+x5+x6+x7+x8+x9+x10+x11+x12+x13+x14+x15+x16+x17+x18+x19+x20+x21+x22+x23+x24+x25) <= C)
            nlp.Minimize(z)
            nlp.solve(disp=False)
            
            result.append('x1: '+ str(x1.value[0]))
            result.append('x2: '+ str(x2.value[0]))
            result.append('x3: '+ str(x3.value[0]))
            result.append('x4: '+ str(x4.value[0]))
            result.append('x5: '+ str(x5.value[0]))
            result.append('x6: '+ str(x6.value[0]))
            result.append('x7: '+ str(x7.value[0]))
            result.append('x8: '+ str(x8.value[0]))
            result.append('x9: '+ str(x9.value[0]))
            result.append('x10: '+ str(x10.value[0]))
            result.append('x11: '+ str(x11.value[0]))
            result.append('x12: '+ str(x12.value[0]))
            result.append('x13: '+ str(x13.value[0]))
            result.append('x14: '+ str(x14.value[0]))
            result.append('x15: '+ str(x15.value[0]))
            result.append('x16: '+ str(x16.value[0]))
            result.append('x17: '+ str(x17.value[0]))
            result.append('x18: '+ str(x18.value[0]))
            result.append('x19: '+ str(x19.value[0]))
            result.append('x20: '+ str(x20.value[0]))
            result.append('x21: '+ str(x21.value[0]))
            result.append('x22: '+ str(x22.value[0]))
            result.append('x23: '+ str(x23.value[0]))
            result.append('x24: '+ str(x24.value[0]))
            result.append('x25: '+ str(x25.value[0]))


            #print('   d: '+ str(d.value[0]))
            print('Objective: ' + str(nlp.options.objfcnval))

            #print('----->',d11)
            #print('->',d3)

        def optimizer3(C,N): 
            from gekko import GEKKO as gk
            import math
            nlp = gk(remote=False)

            nlp.options.SOLVER=1  # APOPT is an MINLP solver


            # defining variables

            x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16,x17,x18,x19,x20,x21,x22,x23,x24,x25,x26,x27,x28,x29,x30,x31,x32,x33,x34,x35 = nlp.Array(nlp.Var,35,lb=0,ub=1,integer=True)
            #x_list=[]
            #a_list=[]
            #d_list=[]
            
            # for i in range(1,num+1):
            #  x_list.append('x'+str(i))
            #for i in range(1,num+1):
            #   a_list.append('x'+str(i))
            #for i in range(1,num+1):
            #   d_list.append('x'+str(i))

            #for l in x_list:
            #   l = nlp.Array(nlp.Var,1,lb=0,ub=1,integer=True)
            #   print(l)
            #o=0
            #for m in a_list:
            #  m = dist_from_base_center[o]
            #  o += 1
            #  print(m)

            d1=dist_from_base_refnode[0]
            d2=dist_from_base_refnode[1]
            d3=dist_from_base_refnode[2]
            d4=dist_from_base_refnode[3]
            d5=dist_from_base_refnode[4]
            d6=dist_from_base_refnode[5]
            d7=dist_from_base_refnode[6]
            d8=dist_from_base_refnode[7]
            d9=dist_from_base_refnode[8]
            d10=dist_from_base_refnode[9]
            d11=dist_from_base_refnode[10]
            d12=dist_from_base_refnode[11]
            d13=dist_from_base_refnode[12]
            d14=dist_from_base_refnode[13]
            d15=dist_from_base_refnode[14]
            d16=dist_from_base_refnode[15]
            d17=dist_from_base_refnode[16]
            d18=dist_from_base_refnode[17]
            d19=dist_from_base_refnode[18]
            d20=dist_from_base_refnode[19]
            d21=dist_from_base_refnode[20]
            d22=dist_from_base_refnode[21]
            d23=dist_from_base_refnode[22]
            d24=dist_from_base_refnode[23]
            d25=dist_from_base_refnode[24]
            d26=dist_from_base_refnode[25]
            d27=dist_from_base_refnode[26]
            d28=dist_from_base_refnode[27]
            d29=dist_from_base_refnode[28]
            d30=dist_from_base_refnode[29]
            d31=dist_from_base_refnode[30]
            d32=dist_from_base_refnode[31]
            d33=dist_from_base_refnode[32]
            d34=dist_from_base_refnode[33]
            d35=dist_from_base_refnode[34]

            
            #incentive coeff for objective function
            a1=dist_from_base_center[0]
            a2=dist_from_base_center[1]
            a3=dist_from_base_center[2]
            a4=dist_from_base_center[3]
            a5=dist_from_base_center[4]
            a6=dist_from_base_center[5]
            a7=dist_from_base_center[6]
            a8=dist_from_base_center[7]
            a9=dist_from_base_center[8]
            a10=dist_from_base_center[9]
            a11=dist_from_base_center[10]
            a12=dist_from_base_center[11]
            a13=dist_from_base_center[12]
            a14=dist_from_base_center[13]
            a15=dist_from_base_center[14]
            a16=dist_from_base_center[15]
            a17=dist_from_base_center[16]
            a18=dist_from_base_center[17]
            a19=dist_from_base_center[18]
            a20=dist_from_base_center[19]
            a21=dist_from_base_center[20]
            a22=dist_from_base_center[21]
            a23=dist_from_base_center[22]
            a24=dist_from_base_center[23]
            a25=dist_from_base_center[24]
            a26=dist_from_base_center[25]
            a27=dist_from_base_center[26]
            a28=dist_from_base_center[27]
            a29=dist_from_base_center[28]
            a30=dist_from_base_center[29]
            a31=dist_from_base_center[30]
            a32=dist_from_base_center[31]
            a33=dist_from_base_center[32]
            a34=dist_from_base_center[33]
            a35=dist_from_base_center[34]

            #p=0
            #for n in d_list:
            # n = dist_from_base_refnode[p]
            # p += 1
                #print(n)    
        
            d0 = 0.99

            n = 3.61

            z=10*n*nlp.log(d1/d0)*x1*a1 + 10*n*nlp.log(d2/d0)*x2*a2 + 10*n*nlp.log(d3/d0)*x3*a3+10*n*nlp.log(d4/d0)*x4*a4+10*n*nlp.log(d5/d0)*x5*a5+10*n*nlp.log(d6/d0)*x6*a6+10*n*nlp.log(d7/d0)*x7*a7 + 10*n*nlp.log(d8/d0)*x8*a8 + 10*n*nlp.log(d9/d0)*x9*a9 + 10*n*nlp.log(d10/d0)*x10*a10 +10*n*nlp.log(d11/d0)*x11*a11 + 10*n*nlp.log(d12/d0)*x12*a12 + 10*n*nlp.log(d13/d0)*x13*a13+10*n*nlp.log(d14/d0)*x14*a14+10*n*nlp.log(d15/d0)*x15*a15+10*n*nlp.log(d16/d0)*x16*a16+10*n*nlp.log(d17/d0)*x17*a17 + 10*n*nlp.log(d18/d0)*x18*a18 + 10*n*nlp.log(d19/d0)*x19*a19 + 10*n*nlp.log(d20/d0)*x20*a20+10*n*nlp.log(d21/d0)*x21*a21 + 10*n*nlp.log(d22/d0)*x22*a22 + 10*n*nlp.log(d23/d0)*x23*a23+10*n*nlp.log(d24/d0)*x24*a24+10*n*nlp.log(d25/d0)*x25*a25+10*n*nlp.log(d26/d0)*x26*a26+10*n*nlp.log(d27/d0)*x27*a27 + 10*n*nlp.log(d28/d0)*x28*a28 + 10*n*nlp.log(d29/d0)*x29*a29 + 10*n*nlp.log(d30/d0)*x30*a30+10*n*nlp.log(d31/d0)*x31*a31 + 10*n*nlp.log(d32/d0)*x32*a32 + 10*n*nlp.log(d33/d0)*x33*a33+10*n*nlp.log(d34/d0)*x34*a34+10*n*nlp.log(d35/d0)*x35*a35  
            # constraint equation.
        
            nlp.Equation(x1+x2+x3+x4+x5+x6+x7+x8+x9+x10+x11+x12+x13+x14+x15+x16+x17+x18+x19+x20+x21+x22+x23+x24+x25+x26+x27+x28+x29+x30+x31+x32+x33+x34+x35 ==N)
            nlp.Equation(1722*(x1+x2+x3+x4+x5+x6+x7+x8+x9+x10+x11+x12+x13+x14+x15+x16+x17+x18+x19+x20+x21+x22+x23+x24+x25+x26+x27+x28+x29+x30+x31+x32+x33+x34+x35) <= C)
            nlp.Minimize(z)
            nlp.solve(disp=False)
            
            print('   x1: '+ str(x1.value[0]))
            print('   x2: '+ str(x2.value[0]))
            print('   x3: '+ str(x3.value[0]))
            print('   x4: '+ str(x4.value[0]))
            print('   x5: '+ str(x5.value[0]))
            print('   x6: '+ str(x6.value[0]))
            print('   x7: '+ str(x7.value[0]))
            print('   x8: '+ str(x8.value[0]))
            print('   x9: '+ str(x9.value[0]))
            print('   x10: '+ str(x10.value[0]))
            print('   x11: '+ str(x11.value[0]))
            print('   x12: '+ str(x12.value[0]))
            print('   x13: '+ str(x13.value[0]))
            print('   x14: '+ str(x14.value[0]))
            print('   x15: '+ str(x15.value[0]))
            print('   x16: '+ str(x16.value[0]))
            print('   x17: '+ str(x17.value[0]))
            print('   x18: '+ str(x18.value[0]))
            print('   x19: '+ str(x19.value[0]))
            print('   x20: '+ str(x20.value[0]))
            print('   x21: '+ str(x21.value[0]))
            print('   x22: '+ str(x22.value[0]))
            print('   x23: '+ str(x23.value[0]))
            print('   x24: '+ str(x24.value[0]))
            print('   x25: '+ str(x25.value[0]))
            print('   x26: '+ str(x26.value[0]))
            print('   x27: '+ str(x27.value[0]))
            print('   x28: '+ str(x28.value[0]))
            print('   x29: '+ str(x29.value[0]))
            print('   x30: '+ str(x30.value[0]))
            print('   x31: '+ str(x31.value[0]))
            print('   x32: '+ str(x32.value[0]))
            print('   x33: '+ str(x33.value[0]))
            print('   x34: '+ str(x34.value[0]))
            print('   x35: '+ str(x35.value[0]))
            #print('   x36: '+ str(x36.value[0]))
            #print('   d: '+ str(d.value[0]))
            print('Objective: ' + str(nlp.options.objfcnval))

            #print('----->',a36)

        C=cost#int(input('Insert total cost of nodes assigned: '))
        N=nodes#int(input('Insert no of nodes: '))
        if (C>=N*1722):
            if num==15:
                optimizer1(C,N)
                
            elif num==25:
                optimizer2(C,N)
            elif num==35:
                optimizer3(C,N)
        else:
            print('----------/ Sorry! Funds are not sufficient for number of nodes mentioned /----------') 
            print('----------/ please reduce the no. of nodes /----------')  
            print('-----------------------------------------------------') 
            print('Maximum nodes possible with available budget:',int(C/1722))
            N=int(input('Insert no of nodes less than or equal to max possible nodes: '))
            if num==15:
                optimizer1(C,N)
            elif num==25:
                optimizer2(C,N)
            elif num==35:
                optimizer3(C,N)
    opti(slabs,length,breadth,height,cost,nodes)
    return render(request,"base_output.html",{'base_data':result})

    
