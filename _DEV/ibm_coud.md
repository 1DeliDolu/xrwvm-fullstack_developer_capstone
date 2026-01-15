Tabii! İşte senin bu projede yaptığın işlemler ve kullandığın komutların sıralı özeti:

1. Microservice dizinine geçiş
Projede sentiment analyzer servisini içeren dizine girdin:



cd xrwvm-fullstack_developer_capstone/server/djangoapp/microservices
2. Docker imajını oluşturma
Sentiment analyzer uygulamasını Docker imajı olarak build ettin:



docker build . -t us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer
Burada ${SN_ICR_NAMESPACE} senin IBM Container Registry namespace’in.

3. Docker imajını IBM Container Registry’ye push etme
Oluşturduğun Docker imajını IBM Container Registry’ye gönderdin:



docker push us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer
4. Code Engine üzerinde uygulamayı deploy etme
Docker imajını kullanarak Code Engine’de sentianalyzer isimli uygulamayı oluşturup deploy ettin:



ibmcloud ce application create --name sentianalyzer --image us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer --registry-secret icr-secret --port 5000
--port 5000 uygulamanın 5000 portunda çalıştığını belirtir.
--registry-secret icr-secret container registry erişimi için gizli anahtar.
Eğer uygulama zaten varsa, önce silmen veya farklı isim vermen gerekti.

5. Uygulama durumunu kontrol etme
Uygulamanın durumunu ve URL’sini kontrol ettin:



ibmcloud ce application get -n sentianalyzer
veya



ibmcloud ce application list
Bu komutlar ile uygulamanın hazır olup olmadığını ve erişim URL’sini görebilirsin.

6. Sentiment analyzer servisini test etme
Uygulamanın URL’sini kullanarak curl ile test yaptın:



curl -X GET "https://sentianalyzer.255i0mx5miws.us-south.codeengine.appdomain.cloud/analyze/Fantastic%20services"
Bu istekten başarılı şekilde JSON formatında yanıt aldın:



{"sentiment": "positive"}
Özet:
Microservice dizinine geçtin.
Docker imajını build ve push ettin.
Code Engine’de uygulamayı deploy ettin.
Uygulamanın durumunu ve URL’sini kontrol ettin.
Curl ile servisi test ettin ve doğru yanıt aldın.