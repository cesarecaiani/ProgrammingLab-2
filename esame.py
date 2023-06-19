class ExamException(Exception):
    pass

class CSVTimeSeriesFile():
    def __init__(self, name):
        self.name = name
        #provo a verificare nell'init se il file esiste:
        self.can_read = True #true di default

        #provo ad aprire il file e a leggere una riga
        try:
            my_file = open(self.name, 'r')
            my_file.readline()
        except Exception as e:
            self.can_read = False #dico che non sono riuscito a leggere il file
            print('Errore in apertura del file: "{}"'.format(e))

    def get_data(self):

        if not self.can_read:
            #se nell' init ho settato can.read a False vuol dire che il file era illeggibile o non poteva essere aperto
            #alzo un ExamException
            raise ExamException('Errore. File illeggibile o non esistente')

            #esco dalla funzione tornando niente
            return None

        else:
            #inizializzo una lista vuota per salvare i dati
            time_series = []

            #apro il file
            my_file = open(self.name, 'r')
            for line in my_file:
                 #faccio lo slicing su ogni riga ad ogni virgola
                elements = line.split(',')

                #posso anche pulire il carattere di newline dell'ultimo elemento
                elements[-1] = elements[-1].strip()
                if elements[0] != 'date':
                    elements[1] = int(elements[1])
                    time_series.append(elements)

            #faccio il check della time series        
            prev_data=0
            for line in time_series:
                date=line[0]
                date_elements = date.split('-')
                if int(prev_data) > int(date_elements[0]):
                    raise ExamException('Gli anni non sono ordinati in senso crescente')
                else:
                    prev_data=date_elements[0]
                    
            my_file.close()
            #finito di controllare tutte le righe ritorno la lista
            return time_series
            
def compute_avg_monthly_difference(time_series, first_year, last_year):

    #verifico che la time_series non sia vuota
    if time_series == []:
        raise ExamException('Lista "time_series" vuota')

    try:
        first_year = int(first_year)
        last_year = int(last_year)
    except:
        raise ExamException('Errore. Anni non sono nel fomato corretto')

    if first_year < 0 or last_year < 0:
        raise ExamException('Errore. Valore degli anni non valido')
    #verifico subito che first_year sia minore di last_year e che non siano uguali
    if first_year > last_year:
        raise ExamException('Errore. first_year è maggiore di last_year')
    if first_year == last_year:
        raise ExamException('Errore. first_year e lasta_year sono uguali e non ho un intervallo')

    #variabile years per fare dopo verifica dell'esisyenza degli anni nel file
    years = []
    #creo dizionario per salvare i valori dei passeggeri anno per anno
    passeggeri_per_anno={}
    for line in time_series:
        #memorizzo la prima colonno come data
        date = line[0]
        #e la seconda come numero di passeggeri
        passengers = line[1]
        #separo la data in due per dividere anno e mese
        date_elements = date.split('-')
        try: 
            year = int(date_elements[0])
            month = int(date_elements[1])
        except:
            raise ExamException('Errore. Valore di mese e anno non valido')
        try:
            years.append(year)
        except:
            raise ExamException('Errore. Nessun anno aggiunto alla lista')
        #se year è nel range degli anni di riferimento
        if year in range(first_year, last_year + 1):
            #se year non è già presente nel dizionario
            if year not in passeggeri_per_anno:
                #aggiungo al dizionario una lista vuota riferita all'anno con 12 sapazi e con valore iniziale 'None'
                passeggeri_per_anno[year] = [None] * 12
            #per ogni anno aggiugno il numero di passeggieri per ogni mese
            passeggeri_per_anno[year][month - 1] = passengers

    #verifico il caso in cui il dizionario sia vuoto
    if passeggeri_per_anno == {}:
        raise ExamException('Errore. Non sono stati aggiunti file al dizionario')
    
    #verifico che gli anni siano nel file
    if first_year not in years or last_year not in years:
        raise ExamException('Errore. Gli anni non sono validi')

    #creo lista sum_variation per memorizzare la somma dei passeggeri di ogni mese al variare dell'anno
    sum_variation = []
    sum = 0
    #per ogni mese da 0 a 12, dove 0 indica gennaio
    for i in range(0, 12):
        #per ogni anno nel range di riferimento
        for year in range(first_year, last_year):
            #calcolo la differenza dei peasseggeri per ogni mese consecutivo e li sommo alla differenza dei mesi precedenti
            sum = sum + (int(passeggeri_per_anno[year + 1][i]) - int(passeggeri_per_anno[year][i]))
                
        try:
            sum_variation.append(sum)
        except:
            raise ExamException('Errore. Non è stato possibile aggiugnere elemento alla lista')
        #metto di nuovo sum a 0 per ricominciare il ciclo
        sum = 0
        
    #creo lista di supporto in cui memorizzo la media delle variaizoni
    avg_monthly_difference = []
    #per ogni elemento della lista precendete che memorizzava le somme delle variazioni
    for item in sum_variation:
        #calcolo la variazione dei rispettivi mesi in base al numero di anni utilizzati per il calcolo
        variation = item / (last_year - first_year)
        try:
            avg_monthly_difference.append(variation)
        except:
            raise ExamException('Errore. Impossibile aggiungere questo elemento a "avg_monthly"')
    
    return avg_monthly_difference

#esempio di utilizzo:
#time_series_file = CSVTimeSeriesFile(name = 'data.csv')
#time_series = time_series_file.get_data()
#avg_monthly_difference = compute_avg_monthly_difference(time_series, "1949", "1951")
#print(avg_monthly_difference)