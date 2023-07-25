[![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=Планировщик)](https://git.io/typing-svg)
## 📖 О проекте:

Позволяет создавать Доски в которых можно создать как общие коллективные цели, так и собственныею

Также имеется поддержка регистрации через ВК и телеграмм бот.

Сайт: **[instareal.ga](http://instareal.ga/)**

## 🛠 Установка

### 🧾 Требования:

- Python3.10
- Poetry
- Docker

> **Внимание:**
>
> Если вы хотите использовать регистрацию через ВК,
> вам потребуется установить параметры `SOCIAL_AUTH_VK_OAUTH2_KEY` и `SOCIAL_AUTH_VK_OAUTH2_SECRET` в `.env`.
> подробнее как их получить в ***[описании](https://dev.vk.com/mini-apps/management/settings)*** на сайте вк
>
> Для использования телеграм бота вам потребуется установить его токен в `TELEGRAM_BOT_TOKEN` в `.env`.
>
> Подробнее о том как создать телеграм бота с помощью [BotFather](https://core.telegram.org/bots#6-botfather)

## Как запустить

### В папке с проектом в терминале прописать:
```Sh
docker-compose up --build -d
```

>Проект будет доступен по ссылке
>***[http://localhost/](http://localhost/)***

## Как остановить

### В папке с проектом в терминале прописать:
```Sh
docker-compose down
```
