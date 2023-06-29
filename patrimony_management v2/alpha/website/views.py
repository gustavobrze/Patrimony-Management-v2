from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Cliente, Family, Finance, Objectives, Investment, Assets
from . import db
import requests
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from .graphs import generate_graph, pie_graph_bank, pie_graph_class
from time import sleep
import pandas as pd
import plotly.graph_objects as go

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route("/new_client", methods=['GET', 'POST'])
@login_required
def new_client():

    try:
        last_id = Cliente.query.order_by(db.desc(Cliente.id)).first().id

    except:
        pass

    iRm = 0.003659

    if request.method == 'POST':
        data = request.form.to_dict()
        
        #Informações pessoais
        mod_time = datetime.now()
        client_name = data['fName']
        cpf = data['cpf']
        client_bday = data['birthday']
        civilState = data['civilState']
        email = data['inputEmail4']
        phone = data['phone']
        address = data['address']
        occupation = data['occupation']
        workplace = data['workplace']
        investProf = data['investProf']
        txtboxes = list()
        client_bday = datetime.strptime(client_bday,'%Y-%m-%d')
        
        for i in range(1,18):
            txtboxes.append(data[f'tbox{i}'])
        
        if client_name == '':
            flash('Insira o nome do cliente.', category='error')
        
        elif str(client_bday) == '':
            flash('Insira a data de nascimento', category='error')

        else:
            cliente = Cliente(mod_time=mod_time, name=client_name, cpf=cpf, birthday=client_bday,
                            civil_state=civilState, email=email,phone=phone,address=address,
                            occupation=occupation, workplace=workplace, investor_profile= investProf,
                            txt_dict_1=txtboxes[0], txt_dict_2=txtboxes[1], txt_dict_3=txtboxes[2],
                            txt_dict_4=txtboxes[3], txt_dict_5=txtboxes[4], txt_dict_6=txtboxes[5], 
                            txt_dict_7=txtboxes[6], txt_dict_8=txtboxes[7], txt_dict_9=txtboxes[8], 
                            txt_dict_10=txtboxes[9], txt_dict_11=txtboxes[10], txt_dict_12=txtboxes[11], 
                            txt_dict_13=txtboxes[12], txt_dict_14=txtboxes[13], txt_dict_15=txtboxes[14], 
                            txt_dict_16=txtboxes[15], txt_dict_17=txtboxes[16], user_id=current_user.id)    
        
        #Estrutura Familiar
        nFamily = int(data['nFamily'])
        family = dict()
        fams = list()
        if nFamily >= 1:
            for i in range(1, nFamily+1):
                family[f'nome-{i}'] = data[f'nome-{i}']
                family[f'parentesco-{i}'] = data[f'parentesco-{i}']
                family[f'data-nascimento-{i}'] = datetime.strptime(data[f'data-nascimento-{i}'],'%Y-%m-%d')
                family[f'regime-casamento-{i}'] = data[f'regime-casamento-{i}']

                if family[f'nome-{i}'] == '':
                    flash(f'Insira o nome do familiar {i+1}', alert='error')
                elif family[f'data-nascimento-{i}'] == '':
                    flash(f'Insira a data de nascimento do familiar {i+1}', alert='error')
                else:
                    fam = Family(name=family[f'nome-{i}'], parenthood=family[f'parentesco-{i}'],
                                birthday=family[f'data-nascimento-{i}'], marriage=family[f'regime-casamento-{i}'],
                                cliente=cliente)
                    fams.append(fam)
        
        #Ativos Financeiros
        nAssets = int(data['nAssets'])
        assets = dict()
        assets_list = list()
        if nAssets >= 1:
            for i in range(1, nAssets + 1):
                assets[f'asset-{i}'] = data[f'asset-{i}']
                assets[f'assetType-{i}'] = data[f'assetType-{i}']
                assets[f'assetValue-{i}'] = float(data[f'assetValue-{i}'].replace('.','').replace(',','.'))
                assets[f'bank-{i}'] = data[f'bank-{i}']

                if assets[f'asset-{i}'] == '':
                    flash(f'Insira o nome do ativo {i}', category='error')
                elif assets[f'assetValue-{i}'] == '':
                    flash('Insira o valor do ativo', category='error')
                else:
                    asset = Assets(asset_name=assets[f'asset-{i}'], asset_class=assets[f'assetType-{i}'], asset_value=assets[f'assetValue-{i}'], bank=assets[f'bank-{i}'], cliente=cliente)

                    assets_list.append(asset)
        
        #Informações Financeiras
        patrFin = data['patrFin']
        patrImb = data['patrImb']
        totalPatr = data['totalPatr']
        totalPatr = float(totalPatr.replace('.','').replace(',','.'))
        saving = data['saving']
        income = data['income']
        expenses = data['expenses']

        if patrFin == '':
            patrFin = 0

        if patrImb == '':
            patrImb = 0
        
        #Objetivos
        nObj = int(data['nObj'])
        objectives = dict()
        objs_list = list()

        if nObj >= 1:
            for i in range(1, nObj+1):
                objectives[f'obj-{i}'] = data[f'obj-{i}']
                objectives[f'value-{i}'] = data[f'value-{i}']
                objectives[f'months-{i}'] = data[f'months-{i}']
                objectives[f'priority-{i}'] = data[f'priority-{i}']
                objectives[f'init-{i}'] = data[f'init-{i}']
                objectives[f'mensalCont-{i}'] = data[f'mensalCont-{i}']
                objectives[f'realValue-{i}'] = data[f'realValue-{i}']
                objectives[f'actPlan-{i}'] = data[f'actPlan-{i}']

                if objectives[f'init-{i}'] == '':
                    objectives[f'init-{i}'] = 0
                
                if objectives[f'value-{i}'] == '':
                    flash(f'Insira o valor do objetivo {i}', category='error')

                elif objectives[f'months-{i}'] == '':
                    flash(f'Insira o prazo do objetivo {i}', category='error')

                elif objectives[f'realValue-{i}'] == '':
                    flash(f'Insira o valor do aporte real do objetivo {i}', category='error')
                else:
                    objs = Objectives(objective=objectives[f'obj-{i}'], value=objectives[f'value-{i}'],
                                    time = objectives[f'months-{i}'], priority=objectives[f'priority-{i}'],
                                    initValue=objectives[f'init-{i}'], monthValue = objectives[f'mensalCont-{i}'],
                                    realValue=objectives[f'realValue-{i}'], actPlan=objectives[f'actPlan-{i}'], cliente=cliente)
                    
                    objs_list.append(objs)

        #Independência Financeira
        
        retAge = data['retAge']
        desIncome = data['desIncome']
        initCont = data['initCont']
        cont = data['cont']
        realCont = data['realCont']
        indepActPlan = data['indepActPlan']
        
        if retAge == '':
            flash('Insira a idade desejada de aposentadoria.', category='error')

        elif desIncome == '':
            flash('Insira a renda desejada na aposentadoria.', category='error')
            
        elif initCont == '':
            flash('Insira a contribuição inicial.', category='error')
            
        elif income == '':
            flash('Insira a receita mensal do cliente.', category='error')

        elif expenses == '':
            flash('Insira a desepesa mensal do cliente', category='error')
        
        else:
            
            db.session.add(cliente)

            try:
                for fam in fams:
                    db.session.add(fam)

            except:
                pass
            
            try:
                for asset in assets_list:
                    db.session.add(asset)
            except:
                pass
            
            finances = Finance(patrFin=patrFin, patrImb=patrImb,
                            saving=saving, income=income,
                            expenses=expenses, totalPatr=totalPatr, cliente=cliente)
            
            db.session.add(finances)

            try:
                for obj in objs_list:
                    db.session.add(obj)
            except:
                pass
            
            investment = Investment(retAge=retAge, desIncome=desIncome, initCont=initCont, monthCont=cont, realCont=realCont, indepActPlan=indepActPlan, cliente=cliente)

            db.session.add(investment)

            db.session.commit()

        sleep(5)

    return render_template("new_client.html", user=current_user, rate=iRm, id = last_id)

@views.route("/report/<int:id>", methods=['GET', 'POST'])
@login_required
def graphs(id):
    
    today = datetime.strftime(datetime.today(), '%d/%m/%Y')

    objectives = Objectives.query.filter_by(cliente_id=id).all()

    graphs = list()
    
    invest = Investment.query.filter_by(cliente_id=id).first()

    finance = Finance.query.filter_by(cliente_id=id).first()

    client = Cliente.query.filter_by(id=id).first()

    name = client.name
    retAge = invest.retAge
    civSt = client.civil_state
    pl = finance.patrFin
    saving = finance.saving
    client_bday = client.birthday
    profile = client.investor_profile
    desIncome = invest.desIncome
    age = relativedelta(datetime.today(), client_bday).years
    
    clientData = dict()
    clientData['name'] = name
    clientData['profile'] = profile
    clientData['age'] = age
    clientData['retAge'] = retAge
    clientData['civSt'] = civSt
    clientData['pl'] = pl
    clientData['saving'] = saving
    
    try:
        family = Family.query.filter_by(cliente_id=id).all()
        filho = 1
        for fam in family:
            famname = fam.name
            if fam.parenthood == 'conjuge':
                clientData['conjuge'] = famname
            elif fam.parenthood == 'filho':
                clientData[f'filho_{filho}'] = famname
                filho += 1
    except:
        pass


    time = (invest.retAge - age) * 12
    initValue = invest.initCont
    monthValue = invest.monthCont
    realCont = invest.realCont
    pl_ideal = round(desIncome/0.003659,2)
    indepActPlan = invest.indepActPlan
    
    plot_ind = generate_graph('Independência Financeira', initValue, monthValue, realCont, time, 0.003659)
    
    indep = [plot_ind[0], str(time/12)[:-2], "{:,.0f}".format(initValue).replace(",", "."),
             "{:,.0f}".format(monthValue).replace(",", "."), "{:,.0f}".format(realCont).replace(",", "."),
             "{:,.0f}".format(pl_ideal).replace(",", "."), "{:,.0f}".format(desIncome).replace(",", "."),
             "{:,.0f}".format(round(plot_ind[1],2)).replace(",", "."), "{:,.0f}".format(round(plot_ind[1] * 0.003659, 2)).replace(",", "."),
             indepActPlan]

    obj_data = list()

    for i in objectives:

        obj = i.objective
        time = i.time
        initValue = i.initValue
        realValue = i.realValue
        monthValue = i.monthValue
        actPlan = i.actPlan

        plot_html = generate_graph(obj, initValue, monthValue, realValue, time, 0.003659)

        if time >= 24:
            time = str(time/12)[:-2] + ' anos'
        else:
            time = str(time)[:-2] + ' meses'

        obj_data.append([obj, time, "{:,.0f}".format(initValue).replace(",", "."), "{:,.0f}".format(realValue).replace(",", "."),
                         "{:,.0f}".format(monthValue).replace(",", "."),"{:,.0f}".format(round(plot_html[1],2)).replace(",", "."),
                         actPlan])

        graphs.append(plot_html[0])

    return render_template('reports.html', today=today, user=current_user, objs=zip(obj_data, graphs), clientData=clientData, indep=indep)

@views.route("/client_list", methods=['GET', 'POST'])
@login_required
def client_list():
    
    clientes = Cliente.query.filter_by(user_id=current_user.id).all()

    return render_template('client_list.html', clientes=clientes, user=current_user)

@views.route("/allocation/<int:id>", methods=['GET', 'POST'])
@login_required
def allocation(id):

    today = datetime.strftime(datetime.today(), '%d/%m/%Y')

    cliente_id = id

    assets = Assets.query.filter_by(cliente_id=cliente_id).all()

    df = pd.DataFrame()

    classes = list()
    values = list()
    banks = list()

    try:
        for asset in assets:
            classes.append(asset.asset_class)
            values.append(asset.asset_value)
            banks.append(asset.bank)

            temp = pd.DataFrame({'Classe':classes, 'Valor':values, 'Instituição':banks})

            df = pd.concat([df,temp])

        pie_bank = pie_graph_bank(df)

        pie_class = pie_graph_class(df)
    
    except:
        pass

    return render_template("allocation.html", today=today, pie_bank=pie_bank, df=df, pie_class=pie_class, user=current_user, cliente_id=cliente_id)
@views.route("/suggestion/<int:id>", methods=['GET', 'POST'])
@login_required
def suggestion(id):

    today = datetime.strftime(datetime.today(), '%d/%m/%Y')

    cliente_id = id

    assets = Assets.query.filter_by(cliente_id=cliente_id).all()

    df = pd.DataFrame()

    classes = list()
    values = list()
    banks = list()

    total_value = 0
    try:
        for asset in assets:
            classes.append(asset.asset_class)
            values.append(asset.asset_value)
            banks.append(asset.bank)

            temp = pd.DataFrame({'Classe':classes, 'Valor':values, 'Instituição':banks})

            df = pd.concat([df,temp])
    except:
        pass

    for v in df['Valor']:
        total_value += v

    classes = ['Conta Corrente', 'CDI POS', 'CDI PRE', 'Inflação', 'COE', 'Multimercado', 'Fundo imobiliário', 'Ação', 'Hedge', 'Internacional', 'PGBL', 'VGBL', 'Outro']

    return render_template("suggestion.html", classes=classes, total_value=total_value, df=df, user=current_user, today=today)