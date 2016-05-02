__author__ = 'omar'


import numpy as np
from decimal import Decimal
import math
#--------------------------------------------------------------------------SAVE DICTIONARY
def save_DICT_data_as_csv(data_dict,filename):
    import csv

    csv_columns = data_dict.keys()
    unformat_data = data_dict.values()
    sample_size = len(unformat_data[0])

    dict_data = []
    for j in range(0,sample_size):
        tmp_dict={}
        for system in range(0,len(csv_columns)):
           tmp_dict[csv_columns[system]]=unformat_data[system][j]
        print tmp_dict
        dict_data.append(tmp_dict)

    try:
        with open(filename, 'wb') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError as (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))
    return

# ----------------------------------------------------------------------LOAD DICTIONARY FROM CSV
def load_DICT_data_from_csv(csv_file):
    import csv
    try:
            with open(csv_file) as csvfile:
                reader = csv.DictReader(csvfile)
                temp= True
                system_name = {}
                system_data = []
                for row in reader:
                    if (temp):
                        system_name= row.keys()
                        temp = False
                        for i in range(0,len(system_name)): system_data.append([])
                    for i in range(0,len(system_name)):
                       system_data[i].append(row[system_name[i]])
                    #print row['Row'], row['Name'], row['Country']
                r_data = {}
                for i in range(0,len(system_name)):
                    r_data[system_name[i]]= np.array([float(a) for a in system_data[i]])

    except IOError as (errno, strerror):
                print("I/O error({0}): {1}".format(errno, strerror))

    return r_data



#-----------------------------------------------------------------save single dictionary

def save_single_dictionary(dictionary,filename):
    import csv

    w = csv.writer(open(filename, "w"))
    for key, val in dictionary.items():
        w.writerow([key, val])
#------------------------------------------------------------------load single dictionary
def load_single_dictionary(filename):
    import csv
    dict = {}
    for key, val in csv.reader(open(filename)):
        dict[key] = val

    return dict
#------------------------------------------------------------------ buil conclusion CMP system

def build_conclusion(summary):

        TITLE_ROW= ['COMPARING SYSTEMS','Number Observation','Sample Mean','Sample Variance','Sample SD','Range','Confidence interval']

        Note = "-"*100 +"\n NOTE : \n This test consists of determining a confidence interval (CI) of difference sample data and simply  \n"
        Note += " checking if the interval include zero. In the case of CI includes zero, the measured values are not \n"
        Note += " significantly different from zero, and therefore, the two systems compared are not different. In the \n"
        Note += " other hand, in case of CI don't include zero the measured value is significantly different from zero, \n"
        Note += " and therefore, one system is better than the other, depending of the sign of mean. "
        Note +="\n"+"-"*100 +"\n"
        conclusion = "*"*80 +"\n   CONCLUSION : \n" + "*"*80 + "\n" + Note
        n_cmp=len(summary)
        include_zero_count=0
        include_zero_cmp= []
        better_list = []
        worst_list =[]
        sys_reference=""
        better_count =0
        worst_count =0
        for i in range(n_cmp):
            row = summary[i]
            cmp_title = row['COMPARING SYSTEMS']
            systems = cmp_title.split('x',1)
            sys_reference =systems[0]
            system2 =systems[1]
            mean= row['Sample Mean']
            range1 = row['Range']
            if (mean - range1<0 and mean + range1>0):
             include_zero_count +=1
             include_zero_cmp.append( cmp_title)
            else:
                if mean>0:
                   better_count +=1
                   better_list.append(system2)
                else:
                   worst_count+=1
                   worst_list.append(system2)

        #print include_zero_cmp,better_list,worst_list

        if(len(include_zero_cmp)>0):
            conclusion+= " The confidence interval of comparisons : " + str(include_zero_cmp) + " \n includes zero. " \
                                                                                                "Therefore, the compared systems are not significantly different and we can not say  \n"
            conclusion+= " anything about which algorithm is better. \n"
        if(len(better_list)>0):
            conclusion+=  " We can say with 95% confidence that the performance of reference system " + str(sys_reference) + ", it is significantly greater \n than the systems :" + str(better_list) + ". \n"
        if(len(worst_list)>0):
            conclusion+= " The performance of the reference system " + str(sys_reference) + " is worst than the systems:"+ str(worst_list) + ". \n"
        conclusion+="\n" + "*"*80
        return conclusion

# summary table
#------------------------------------------------------------------- summary _cmp_system
def print_summary_table(summary,show_detail =True) :
    v_line="-"*116
    str_summary= v_line + "\n" + "|" +" "*53 +"SUMMARY"+" "*54 + "|\n"

    TITLE_ROW= ['COMPARING SYSTEMS','Number Observation','Sample Mean','Sample Variance','Sample SD','Range','Confidence interval']
    cmp_number=len(summary)
    column_number =len(TITLE_ROW)
    #print cmp_number
    for row in range(-1,cmp_number):
        str_row = "| "
        if (row ==0 or row==-1):
            # if show_detail:
            #      print(v_line)
            # else:
                str_summary += v_line + "\n"


        for col in range(0,column_number):
            dicc_row = summary[row]
            category = TITLE_ROW[col]
            str_tmp =[]
            if col==0 or col==column_number-1:
                str_tmp= category if row==-1 else str(dicc_row[category])
            else:
                str_tmp= category if row==-1 else str('%0.3f'%(dicc_row[category]))

            n = len(category)-len(str_tmp)
            elem = " "*n + str_tmp
            str_row +=elem
            str_row += " | "

              #str_row += "  |"

        # if show_detail: print (str_row)
        # else:
        str_summary += str_row + "\n"
    str_summary += v_line + "\n"
    if show_detail:
        print(str_summary)
    else:
        return str_summary

#------------------------------------------------------------------------------------save summary as csv
def save_summary_data_as_csv(list_dict,filename):
    import csv
    csv_columns = ['COMPARING SYSTEMS','Number Observation','Sample Mean','Sample Variance','Sample SD','Range','Confidence interval']

    #csv_columns = list_dict[0].keys()
    #csv_columns.reverse()
    try:
        with open(filename, 'wb') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in list_dict:
                writer.writerow(data)
    except IOError as (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))
    return

    # with open('mycsvfile.csv', 'wb') as f:  # Just use 'w' mode in 3.x
    #     w = csv.DictWriter(f, data_dict.keys())
    #     w.writeheader()
    #     w.writerow(data_dict)

#------------------------------------------------------------------------------------------ load summary from csv
def load_summary_data_from_csv(csv_file):
    import csv
    try:
            with open(csv_file) as csvfile:
                reader = csv.DictReader(csvfile)
                temp= True
                system_name = {}
                system_data = []
                i=0
                r_data=[]
                for row in reader:
                    r_data.append(row)
                #     if (temp):
                #         system_name= row.keys()
                #         temp = False
                #         for i in range(0,len(system_name)): system_data.append([])
                #     for i in range(0,len(system_name)):
                #        system_data[i].append(row[system_name[i]])
                #     #print row['Row'], row['Name'], row['Country']
                # r_data = {}
                # for i in range(0,len(system_name)):
                #     r_data[system_name[i]]= np.array([float(a) for a in system_data[i]])

    except IOError as (errno, strerror):
                print("I/O error({0}): {1}".format(errno, strerror))

    return r_data
#-------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
# CMP SYSTEM
def cmp_system_paired(sys_1,sys_2,data1,data2,summary=[],show_detail =True):

    #  1     MEAN Y1 and Y2
    mean_data1 = np.mean(data1)
    mean_data2 = np.mean(data2)
    n_data = len(data1)
    summary_row={}
    current_cmp =""
    #  2     deference % values of matched pairs

    dif_data = np.array(data1-data2)
    mean_dif = np.mean(dif_data)

    # 3  with 95% confidence interval z-variare (1.960)

    #
    v_z = 1.960    # 95%
    #v_z = 2.576     # 99%

    # 4  standard deviation   s= 1/n-1 sumatoria de (xi-mean)2

    suma_data =0
    for i in (dif_data  - mean_dif):
      suma_data += i**2

    sample_variance = suma_data/(n_data-1)
    standard_deviation = math.sqrt(sample_variance)

    # 5  confidence interval

    sqrt_n_data=math.sqrt(n_data)
    range_i= v_z *standard_deviation/sqrt_n_data

    r_inf,r_sup = mean_dif-range_i,mean_dif+range_i

    # build row summary
    summary_row['COMPARING SYSTEMS']=(sys_1 + ' x ' + sys_2)
    summary_row['Number Observation'] = n_data
    summary_row['Sample Mean']= mean_dif
    summary_row['Sample Variance']=sample_variance
    summary_row['Sample SD']=standard_deviation
    summary_row['Range']= range_i
    summary_row['Confidence interval']= str('(%0.4f , %0.4f)'%(r_inf,r_sup))
    if show_detail:
        print '    COMPARING SYSTEMS    :  ' + sys_1 + '  -  ' + sys_2
        print '---95% confidence interval----------------------------------------------------'
        print '    Number of Observation:   %d '%Decimal(n_data)
        print '              Sample mean:   %.5f '%Decimal(mean_dif)
        print '          Sample variance:   %.5f '%Decimal(sample_variance)
        print 'Sample standard deviation:   %.5f '%Decimal(standard_deviation)
        print('      Confidence interval: ( %0.3f +- %0.3f):( %0.3f, %0.3f )'%(mean_dif,range_i,r_inf,r_sup))
        print '------------------------------------------------------------------------------'
    else:
        current_cmp =  "     COMPARING SYSTEMS   :   " + sys_1 + "  -  " + sys_2 + "\n"
        current_cmp += "---95% confidence interval----------------------------------------------------\n"
        current_cmp += "    Number of Observation:   " + str('%d '%Decimal(n_data)) + "\n"
        current_cmp += "              Sample mean:   " + str('%.5f '%Decimal(mean_dif)) + "\n"
        current_cmp += "          Sample variance:   " + str('%.5f '%Decimal(sample_variance)) + "\n"
        current_cmp += "Sample standard deviation:   " + str('%.5f '%Decimal(standard_deviation)) + "\n"
        current_cmp += "      Confidence interval:   " + str('( %0.3f +- %0.3f):( %0.3f, %0.3f )'%(mean_dif,range_i,r_inf,r_sup)) + "\n"
        current_cmp += "------------------------------------------------------------------------------\n"


    # print ' DETERMINING SAMPLE SIZE'
    # # N = 100 * Z *S / R M   Z---%  S-standard deviation , r %  accuracy of metric, m :_x
    #
    # r = 0.01    # r %  accuracy of metric
    # N= 100*v_z*standard_deviation/r*mean_dif
    # print 'Total observation needed:',N**2
    # print '-----------------------------------------------------------------------------------'
    summary.append(summary_row)

    if show_detail:
        return mean_dif, range_i
    else:
        return mean_dif, range_i,current_cmp
#  dictionary
#----------------------------------------------------------------------------------cmp systems
#######################################################################################################################################################33

def get_cmp_system_vs_all(sys_reference,data_dict, save_summary=False,outputdir_csv = "csv/"):

    cmp_details = "            ################ COMPARING SYSTEMS ###############                    \n"
    cmp_details += "------------------------------------------------------------------------------\n"

    if sys_reference in data_dict:
      #------------------------------------------load data
      sample_size=len(data_dict[sys_reference])
      cmp_resul=[]    # all statistical values, list of of (mean,rangei)
      name_cmp = []   # cmp name list (example :['ORB x STAR', 'ORB x HARRIS3D'])
      dif_cmp= []     # cmp difference (list of -list difference between 2 data- )

      cmp_summary=[]
      for systems in data_dict:
          if sys_reference != systems:
              name_cmp.append(sys_reference + " x " + systems) # text cmp
              mean,rangei,detail = cmp_system_paired(sys_reference,systems,data_dict[sys_reference],data_dict[systems],cmp_summary,False)
              cmp_resul.append((mean,rangei))
              cmp_details +=detail
              dif_cmp.append(np.array(data_dict[sys_reference]-data_dict[systems]))

      #
      # save csv table summary
      if save_summary:
          file=outputdir_csv + "cmp_summary_"+sys_reference+".csv"
          save_summary_data_as_csv(cmp_summary,file)

      summary =  print_summary_table(cmp_summary,False)
      cmp_details +=summary
      conclus = build_conclusion(cmp_summary)


      # name_cmp    # cmp name list (example :['ORB x STAR', 'ORB x HARRIS3D'])
      # dif_cmp     # cmp difference (list of -list difference between 2 data- )
      # cmp_resul   # all statistical values, list of tuple (mean,rangei)
      # cmp_details : process details (string)
      # cmp_summary  : dictionary with all statistical values of each cmp
      # conclus : conclusion (string)
      return name_cmp,dif_cmp,cmp_resul,cmp_details,cmp_summary,conclus



#------------------------------------------------------------------------------------------------------------------------


def get_factor_impact(data,rep,alg_name="ANY",show_detail =True):


    # build conclusion
    def build_conclusion(var_name,var_value,fve_min,fve_MAX):

        Note = "-"*100 +"\n NOTE : \n The importance of each factors can be expressed as a fraction;for example : \n  "
        Note += " "*10 + "Fraction of variation explained by factor " + str(' %s = SS_%s/SS_TV . \n'%(var_name[0],var_name[0]))
        Note += " When expressed as percentage, these fractions provides an easy way to gauge the importance of each factors. "
        Note += " \n The factors witch explain a high percentage of variation are considered important in the system performance. "
        Note += " \n   It must be pointed out that the \"variation\" is different from \"variance\". Thus, a factor that explains 30%  \n"
        Note += " of variation may or may not explain 30% of the total variance of responses(Y). The percentage of variance explained  \n"
        Note += " is rather difficult to compute. The percentage of variation, on the other hand, is easy to compute and easy to explain \n"
        Note += " to decision markers. "
        Note +="\n"+"-"*100 +"\n"

        #print var_value
        # processing values
        name_q =["q0"]
        for i in range(0,len(var_name[:-1])):
            name_q.append("q"+var_name[i])

        range_inter = (fve_MAX[0] -fve_min[0])/2
        interv_str = []

        include_zero_count =0
        include_zero_var = []
        for i in range(len(fve_min)):
          if (fve_min[i]<0 and fve_MAX[i]>0):
             include_zero_count +=1
             include_zero_var.append( name_q[i])
          str1 = str('(%0.4f,%0.4f)'%(fve_min[i],fve_MAX[i]))
          interv_str.append(str1)

        str_tmp = "\n Since none of the intervals include a zero, all effects are significantly different from zero at this confidence level."
        str_tmp1= "\n Since the intervals of the effects " + str(include_zero_var) + " include a zero, this effects are not significantly different from zero at this confidence level."
        comment = str_tmp if include_zero_count==0 else str_tmp1
        SST = sum(var_value)
        fraction = var_value/SST *100
        num_values = len(var_value)
        imp_factors = ""
        imp_percentage = ""
        lim_perc=10
        for i in range(num_values):
            if fraction[i]>lim_perc:
                imp_factors +=  str(' %s,'%(var_name[i]))
                imp_percentage += str(' %0.2f,'%(fraction[i]))

        ci = "\n \n The confidence intervals for the parameters are qi +-" + str('%0.5f .'%(range_inter))
        ci += "\n That is, " + str(interv_str) + " \n for " + str(name_q) + " respectively."
        conclusion = "*"*100 +"\n   CONCLUSION : \n" + "*"*100 + "\n" + Note
        conclusion += " Thus, the total variation (SS_TV) of " + str('%0.4f'%(SST)) + " can be divided into " + str(num_values)+ " parts.\n"
        conclusion += " Factor " + var_name[0] + " explains " + str('SS_%s/SS_TV =%0.4f/%0.4f,'%(var_name[0],var_value[0],SST)) + " or " + str('%0.2f'%(fraction[0])) +"%, of the variation. Similary, factor " + var_name[1] + " explains " + str('%0.2f'%(fraction[1])) +"%, and so on."
        conclusion += " \n All variation explained by the factors and its combinations : " + str(var_name[:-1]) + " are showed above in table : FRACTION VARIATION EXPLAINED. \n"
        conclusion += " The remaining " + str('%0.2f'%(fraction[num_values-1])) + "% is unexplained and is attributed to errors."
        conclusion += " \n Them, the factors with more impact or most important (> 10%) in our system are :  " + imp_factors + " with " + imp_percentage + " percentage respectively."

        conclusion+=ci
        conclusion+= comment
        conclusion+= "\n\n" +"*"*100
        return conclusion
    #---------------------------------------------------------------------
    def print_factor_values(levels,s_detail =True):

        local_detail = ""
        factors_d=["Factor","T: Translation (cm)","S: Scale variation (cm)","R: Rotation (degrees)"]
        #level_1 = ["Level -1"] + map(lambda x: str(x[0]),levels)
        levels_s= {0:["Level -1"] + map(lambda x: str(x[0]),levels),1:["Level 1"] + map(lambda x: str(x[1]),levels)}

        for row in range(0,4):
          str_row = "| "
          if (row == 0 or row ==1 ):
              local_detail +="-"*60 + "\n"
          for col in range(0,3):
               str_tmp=""
               if col==0:
                   elem = " "*30
                   str_tmp=str(factors_d[row])
               else:
                   elem = " "*10
                   str_tmp=str(levels_s[col-1][row])
               n= len(elem)-len(str_tmp)
               elem = str_tmp +" "*n
               str_row += elem
               str_row += " | "
          #str_row += " |"
          local_detail +=str_row + "\n"
          local_detail +="-"*60 + "\n"
        if(s_detail):
            print local_detail
        else: return local_detail
    #----------------------------------------------------------------------------
    def print_Sign_table(Matrix,s_detail =True):
        r,c= (r,c)= np.shape(Matrix)
        local_detail = ""
        for row in range(0,r):
          str_row = "|"
          if (row ==1 or row==9 or row==0):
              local_detail +="----------------------------------------------------------------------------------------\n"
          for col in range(0,c):
               elem = "         "
               str_tmp=str(Matrix[row][col])
               n= len(elem)-len(str_tmp)
               if (col==8):
                  str_row += "  |"
               elem = " "*n + str_tmp
               str_row +=elem
          str_row += "  |"
          local_detail +=str_row + "\n"
        local_detail +="----------------------------------------------------------------------------------------\n"
        if(s_detail):
            print local_detail
        else: return local_detail
    #---------------------------------
    def print_ALLOCATION_table(var_name,var_descrip,var_values,title,imp=1,s_detail =True):
        local_detail =""
        TITLE_ROW = title
        lelem = [" "*20," "*25," "*17]
        v_line="-"*72 + "\n"
        for row in range(-1,len(var_name)):
          str_row = "| "
          #print row
          if (row ==0 or row==-1):
              local_detail +=v_line

          for col in range(0,3):

                   if col==0:
                      str_tmp=TITLE_ROW[col]if row==-1 else str(var_name[row])
                   if col==1:
                      str_tmp=TITLE_ROW[col]if row==-1 else str(var_descrip[row])
                   if col==2:
                      str_tmp=TITLE_ROW[col]if row==-1 else str(var_values[row])

                   n = len(lelem[col])-len(str_tmp)

                   elem = " "*n + str_tmp
                   str_row +=elem
                   str_row += " | "

              #str_row += "  |"
          local_detail+=str_row + "\n"
        local_detail+= v_line
        if(imp):
            #str_row = "| " + " "*6 + " "*42 + " |"
            message = " * IMPORTANT *"
            str_row = "| " + message+ " "*(68 - len(message))+ " |"
            local_detail+=str_row  + "\n"
            msg = " SS_TV = " + var_name[3]
            for val in var_name[4:]:
                 msg += "+" + val
            str_row = "| " + msg+ " "*(68 - len(msg))+ " |"
            local_detail+=str_row + "\n"
            local_detail+=v_line + "\n"
        if(s_detail):
            print local_detail
        else: return local_detail
#---------------------------------------------------------------------------------------------
    M1=[1, -1, -1, -1,  1,  1,  1, -1,
                     1,  1, -1, -1, -1, -1,  1,  1,
                     1, -1,  1, -1, -1,  1, -1,  1,
                     1,  1,  1, -1,  1, -1, -1, -1,
                     1, -1, -1,  1,  1, -1, -1,  1,
                     1,  1, -1,  1, -1,  1, -1, -1,
                     1, -1,  1,  1, -1, -1,  1, -1,
                     1,  1,  1,  1,  1,  1,  1,  1]
    M = np.reshape(M1,(8,8))
    factors_combination=['T','S','R','TS','TR','SR','TSR']


    # compute y_mean, totalq

    m_y =[]                               # ARRAY OF MEAN Y..
    t_q =[]                               # M[i] column
    Total_q = []
    y_estimate = []
    for i in range(8):
        sub_m = data[i*rep:i*rep+rep]     # data 10 in 10
        m_y.append(np.mean(sub_m))        # mean of each ten data (mean od d(i))
        t_q.append(M[0:8,i])              # column A,B,C,AB,AC,BC,ABC



    for i in range(8):
        Total_q.append(sum(t_q[i]*m_y))   #tOTAL OF  q[0]  q0,  q[1]  qA,......
    #print 'Total q:',Total_q
    q = map(lambda x: x/8,Total_q)         #tOTAL OF  q[0]  q0,  q[1]  qA,......
    for i in range(8):
       y_estimate.append(sum(q*M[i,0:8]))



    eval_details = "#"*22 +"    2^k*r Factorial Designs         " + "#"*22+ "\n"
    eval_details += "         Algorithm (keypoint detector): " + alg_name + "\n"
    eval_details += "                   Factors to evaluate:  1 - T: Translation (cm)"+ "\n"
    eval_details += "                                         2 - S: Scale variation (cm)"+ "\n"
    eval_details += "                                         3 - R: Rotation (degrees)"+ "\n"
    eval_details += "                        Repetitions (r): " + str(rep) + "\n"
    eval_details += "#"*80 + "\n"
    # --------------------------------------------------------------------------------------------factor levels table
    if show_detail:
        print "\n \n Values factors and levels used:"
        print_factor_values([(0,30),(0,30),(0,15)],1)
    else:
        eval_details += print_factor_values([(0,30),(0,30),(0,15)],0)


    eval_details += "\n"*2 +"#"*33 +"  Prossesing  " + "#"*33 + "\n"*2
    eval_details += " Observed responses (Y): " + str(["%0.4f" % i for i in m_y]) + "\n"
    eval_details += "  Contrasts values (qi): " + str(["%0.4f" % i for i in q]) + "\n"
    eval_details += "  Factors combinations : "  + str(factors_combination) + "\n"
    #eval_details += "#"*80 + "\n"

    # BUILD AND PRINT SIGN TABLE

    m_title = factors_combination[:]
    m_title.insert(0,'I')
    m_title.append("Y")

    Y =  np.empty([10, 9], dtype="S6")
    Y [:,:]="a"
    Y[0,:] = m_title[:]
    Y[1:9,8] = m_y[:]
    Y[1:9,0:8]= np.reshape([str(a) for a in M1],(8,8))
    Y[9,0:8]= q[:]
    Y[9,8] ="T./8"
    #print Y

   # print "  Factors combinations :",factors_combination

    if show_detail:
          print "\n \n     Sign Table Method :"
          print_Sign_table(Y)
    else:
          eval_details += "\n \n     Sign Table Method : \n"
          eval_details += print_Sign_table(Y,0)


    # ESTIMATION OF EXPERIMENTAL ERRORS
    eval_details += "\n"*2 + "-"*22+" ESTIMATION OF EXPERIMENTAL ERRORS  "+ "-"*22 + "\n \n"
    error_R=np.copy(data)
    for i in range(8):
       error_R[i*rep:i*rep+rep] = error_R[i*rep:i*rep+rep]-y_estimate[i]
       #sub_m -= y_estimate[i]

    #print map(lambda x: x**2,error_R)eval_details +=
    SSE = sum(map(lambda x: x**2,error_R))
    eval_details += "Sum os Squared Errors : " + str(SSE) + "\n"

    # -------------------------------------------------------------------------------------------alocation of variation
    eval_details += "\n" * 2 + "-" * 27 + " ALLOCATION OF VARIATION  " + "-" * 27 + "\n \n"

    y_2dot = np.mean(data)
    SSY = sum(map(lambda x: x**2,np.copy(data)))
    SSi=map(lambda x: 8*rep*(x**2),q)
    SST=sum(map(lambda x: (x-y_2dot)**2,np.copy(data)))
    SS = [SSY]+[SST]+SSi+[SSE]

    descrip_variation = ["SUM(Yi^2)","SS_Y-SS_O","8x"+str(rep)+"x q0^2"]
    name_variation =["SS_Y","SS_TV","SS_0"]
    for i in range(0,7):
        descrip_variation.append("8x"+str(rep)+"x q"+factors_combination[i]+"^2")
        name_variation.append("SS_"+factors_combination[i])
    descrip_variation.append("ERROR")
    name_variation.append("SS_E")
    SS_6F=["%0.6f" % i for i in SS]

    #print SS
    title = ["VAR_NAME","DESCRIPTION","VALUE"]
    if show_detail:
          print_ALLOCATION_table(name_variation,descrip_variation,SS_6F,title)
    else:
          eval_details += print_ALLOCATION_table(name_variation,descrip_variation,SS_6F,title,1,0)

    eval_details += "\n" * 2 + "-" * 23 + " FRACTION VARIATION EXPLAINED (%) " + "-" * 23 + "\n \n"
    #eval_details +="\n \n -------- FRACTION VARIATION EXPLAINED (%) --------\n" + "SS_TV:" + str(SST) + "\n"

    FVE= map(lambda x: 100*x/SST,SSi)      #fraction variation_explained

    title = ["VAR_NAME","VALUE"," % OF SS_TV"]

    SS_6F = ["%0.6f" % i for i in SS[3:]]
    SS_6TV = ["%0.6f" % i for i in SS[3:]/SST*100]

    if show_detail:
          print_ALLOCATION_table(name_variation[3:],SS_6F,SS_6TV,title,0)
    else:
          eval_details += print_ALLOCATION_table(name_variation[3:],SS_6F,SS_6TV,title,0,0)

    # print 'fraction variation_explained %------------------------------'
    #
    FVE_error = [100-(sum(FVE)-FVE[0])]
    FVE=np.hstack((FVE,FVE_error))

    eval_details += "\n" * 2 + "-" * 23 + " CONFIDENCE INTERVALS FOR EFFECTS " + "-" * 23 + "\n \n"

    degree=8*(rep-1)
    Se = math.sqrt(SSE/degree)
    sqi=Se/math.sqrt(8*rep)
    eval_details +="\n  Standard Deviation of errors  (Se) : " + str(Se) + "\n"
    eval_details +="  Standard Deviation of effects (Sqi): " + str(sqi) + "\n \n"


    nq = np.array(q)
    from scipy import stats
    alpha=0.1 # 90 %
    t = stats.t._ppf(1 - alpha / 2., degree)
    lim = t * sqi


    msg_t =  "  The t-value at " + str(degree) + " degree of freedom and " + str((1-alpha)*100) + " % confidence is : "  + str(t) +"\n"
    msg_t += "  The confidence intervals for the parameters (Contrasts values) are : \n   Qi +- (t-value)*(Sqi) = Qi +- " + str('(%0.4f)*(%0.4f)'%(t,sqi)) + "= Qi +- " + str(lim)  + "\n \n"
    eval_details += msg_t
    #print 'var:',lim
    fve_min = nq - lim
    fve_MAX = nq + lim
    intervals = []
    name_q =["q0"]
    for i in range(0,len(factors_combination)):
        name_q.append("q"+factors_combination[i])

    for i in range(len(fve_MAX)):
       str1 = str('(%0.4f,%0.4f)'%(fve_min[i],fve_MAX[i]))
       intervals.append(str1)

    q_values= Y[9,0:8]

    title = ["VAR_NAME","VALUE","CONF.INTERV."]

    if show_detail:
          print_ALLOCATION_table( name_q,q_values,intervals,title,0)
    else:
          eval_details += print_ALLOCATION_table( name_q,q_values,intervals,title,0,show_detail)



    #--------------------------------------------------------------------build conclusion
    var_name = factors_combination + ["ERROR"]
    conclusion = build_conclusion(var_name,SS[3:],fve_min,fve_MAX)
    SS_xF = SS[3:]
    if show_detail:
        print eval_details
        print conclusion
    else:
        return eval_details,conclusion,var_name,SS_xF
