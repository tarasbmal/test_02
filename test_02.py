#---------------------------------------------------------------------------------------
#----   Функция получения SECID по параметру, который может быть  SECID,ISIN, Рег.Номеру
#----   а также, параллельно, остальных параметров
#---------------------------------------------------------------------------------------
def micex_get_sec(p_code):
	import pandas as pd
	import datetime 
	#-----   Выгружаем данные с сайта биржи в формате JSON -----
	url = f'https://iss.moex.com/iss/engines/stock/markets/bonds/securities.json?iss.only=securities'
	data = pd.read_json(url)
	#---- преобразуем данные в нормальный фрейм -----
	data = pd.DataFrame(data=data.iloc[1, 0], columns=data.iloc[0, 0])
	#-----  Фильтруем c условием ИЛИ ----
	res = data[(data["SECID"] == p_code) | (data["ISIN"] == p_code) | (data["REGNUMBER"] == p_code)]
	#ret = res['SECID'].max()
	if len(res.index)>0:
		#-- Код бумаги 
		sec_id = res['SECID'].iloc[0]
		#-- Наименование 
		sec_name = res['SECNAME'].iloc[0]
		#-- ISIN
		sec_isin = res['ISIN'].iloc[0]
		#-- Дата погашения
		mat_date = datetime.datetime.strptime(res['MATDATE'].iloc[0], "%Y-%m-%d").date()
		#-- Дата оферты 
		if len(str(res['OFFERDATE'].iloc[0]))>6:
			offer_date = datetime.datetime.strptime(res['OFFERDATE'].iloc[0], "%Y-%m-%d").date()
		else:
			#print(len(str(res['OFFERDATE'].iloc[0])))
			#print(res['OFFERDATE'].iloc[0])
			offer_date = ""						
		#-- Номинал
		nom_sum = res['FACEVALUE'].iloc[0]
		#-- Валюта номинала		
		nom_cur = res['FACEUNIT'].iloc[0]
		#-- Валюта расчетов (SUR- рубли)
		r_cur = res['CURRENCYID'].iloc[0]
		#-- Сумма купона
		coup_sum = res['COUPONVALUE'].iloc[0]
		#-----  Дата ближайшего купона
		coup_date = datetime.datetime.strptime(res['NEXTCOUPON'].iloc[0], "%Y-%m-%d").date()
		#-- % купона - нужно еще делить на 10000
		coup_prc = res['COUPONPERCENT'].iloc[0]
		#-- Период купона 
		coup_period = res['COUPONPERIOD'].iloc[0]
		#-- НКД (Внимание! Сумма НКД для замещающих облигаций, облигаций , номинированных в валюте - в рублях, т.е. нужно пересчитывать в валюту или просто посчитать НКД исходя из размера купона)
		nkd = res['ACCRUEDINT'].iloc[0]
		#-----------------------------------------------------------------------------
		#-- Если скорее всего, замещающая облигация, нужно пересчитывать НКД
		#-----------------------------------------------------------------------------
		if res['FACEUNIT'].iloc[0] != 'SUR' and  res['CURRENCYID'].iloc[0] == 'SUR':	
			#print("Замещающая облигация !!!")			
			#-----  Сегодня 
			buydate = datetime.datetime.today().date()
			#-----  Дней до купона
			days = (coup_date-buydate).days-1
			#-----  Осталось НКД до купона
			left_nkd = (res['FACEVALUE'].iloc[0] * res['COUPONPERCENT'].iloc[0] * days) / 36500
			#----- Расчетный НКД
			nkd = round(res['COUPONVALUE'].iloc[0] - left_nkd,2)	
			#print(nkd)
		#------------------------------------------------------
		#------------------------------------------------------
		#------------------------------------------------------
		ret = sec_id,sec_name,sec_isin,mat_date,offer_date,nom_sum,nom_cur,r_cur,coup_sum,coup_date,coup_prc,coup_period,nkd
	else:
		ret = "","","","","",0,"","",0,"",0,0,0
	return ret

#=======================================================================================
#=======================================================================================
#======    Главная процедура    ========================================================
#=======================================================================================
#=======================================================================================
sec_id,sec_name,sec_isin,mat_date,offer_date,nom_sum,nom_cur,r_cur,coup_sum,coup_date,coup_prc,coup_period,nkd_sum=micex_get_sec('RU000A1041B2')
#sec_id,sec_name,sec_isin,mat_date,nom_sum,nom_cur,r_cur,coup_sum,coup_date,coup_prc,coup_period,nkd_sum=micex_get_sec('111111')
if sec_id == "":
	print('Ценная бумага не найдена !')
else:
	print("sec_id:   " + sec_id)
	print("sec_name: " + sec_name)
	print("sec_isin: " + sec_isin)
	print("mat_date: " + str(mat_date))
	print("offer_date: " + str(offer_date))
	print("nom_sum:  " + str(nom_sum))
	print("nom_cur:  " + nom_cur)
	print("r_cur:    " + r_cur)
	print("coup_sum: " + str(coup_sum))
	print("coup_date:" + str(coup_date))
	print("coup_prc: " + str(coup_prc))
	print("coup_period: " + str(coup_period))
	print("nkd_sum:  " + str(nkd_sum))

