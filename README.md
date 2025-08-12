# Discord Sunucu Kopyalama Tool'u

Bu bot, bir Discord sunucusunun kanallarını, kategorilerini ve rollerini yedekleyip başka bir sunucuya yüklemenizi sağlar.
***Bu 

## Özellikler

- Sunucu kanallarını, kategorilerini ve rollerini JSON formatında yedekler.
- Yedeklenen veriyi başka sunucuya yükleyerek aynı yapılandırmayı oluşturur.
- Yalnızca yönetici yetkisi olan kullanıcılar tarafından kullanılabilir.

## Kurulum

1. Bot tokenınızı [Discord Developer Portal](https://discord.com/developers/applications) üzerinden alın ve botunuzu oluşturun.
2. Botu sunucunuza davet edin ve yönetici yetkisi verin.
3. Kodları indirin ve `cogs` klasörünün içinde `serverclone.py` dosyasının olduğundan emin olun.
4. `bot.py` dosyasını kendi tokenınızla çalıştırın.

## Kullanım

- Sunucuyu yedeklemek için:
!save <yedek_ismi>
- Yedeği yüklemek için:
!load <yedek_ismi>


## Dikkat Edilmesi Gerekenler

- Botun her iki sunucuda da bulunması ve gerekli izinlere sahip olması gerekir.
- `@everyone` rolü otomatik güncellenir, diğer roller ve kanallar yeniden oluşturulur.
- Mesajlar veya dosyalar yedeklenmez, yalnızca sunucu yapısı kopyalanır.
- Komutları kullanmak için yönetici yetkisine sahip olmanız gerekir.

---

**Not:** Bu proje tamamen kişisel kullanım amaçlıdır. Başka sunucularda izinsiz kullanılmamalıdır.

## Sorumluluk Reddi

Bu proje eğitim amaçlı geliştirilmiştir. Kullanıcılar, botu kendi sunucularında ve izin verdikleri sunucularda kullanmalıdır. Başka sunucuların izinsiz kopyalanması yasal ve etik değildir. Kodun sahibi, bu projeyle ilgili doğabilecek herhangi bir sorumluluğu kabul etmez.

## Fork Bilgisi

Bu proje, [ralphrimwell/discord-server-cloner](https://github.com/ralphrimwell/discord-server-cloner) reposundan fork edilerek kendi ihtiyaçları doğrultusunda düzenlenmiştir.
