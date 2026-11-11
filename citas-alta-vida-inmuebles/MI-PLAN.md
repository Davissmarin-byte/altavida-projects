# Mi plan: dónde pego mi liga y cómo doy seguimiento

> Cuando publiques en Vercel, cambia `MI-LIGA.vercel.app` por tu liga real en todo este archivo.
> Lo que va entre corchetes `[ ]` lo llenas tú en cada mensaje.

---

## 1. Mis ligas con etiqueta

Una liga por cada lugar. Así sabes de dónde llega cada cliente.

```
https://MI-LIGA.vercel.app/?origen=instagram
https://MI-LIGA.vercel.app/?origen=whatsapp
https://MI-LIGA.vercel.app/?origen=facebook
https://MI-LIGA.vercel.app/?origen=marketplace
https://MI-LIGA.vercel.app/?origen=inmuebles24
https://MI-LIGA.vercel.app/?origen=referido
https://MI-LIGA.vercel.app/?origen=correo
https://MI-LIGA.vercel.app/?origen=qr
https://MI-LIGA.vercel.app/?origen=grupo
```

**Dónde lo ves:** en tu tablero abre la ficha de la cita, donde dice "Llegó por instagram". También sale en la columna "Llegó por" cuando exportas las citas a Excel.
En un mes ordenas esa columna y sabes qué lugar te trae clientes de verdad.

---

## 2. Textos listos para copiar

### Renglón del perfil de Instagram
```
🏝️ Propiedades en Cancún y Riviera Maya desde $2.5 MDP
📅 Aparta tu cita de compra + asesoría financiera de regalo 👇
https://MI-LIGA.vercel.app/?origen=instagram
```

### Estado de WhatsApp
```
¿Tienes un capital y no sabes dónde ponerlo para que crezca?
Aparta tu cita de compra en Cancún. Te llevas de regalo una asesoría inmobiliaria y financiera y una pre-evaluación de tu crédito.
Elige tu horario aquí 👉 https://MI-LIGA.vercel.app/?origen=whatsapp
```

### Firma de correo
```
Jaime Marín · Alta Vida Inmuebles
Cancún y Riviera Maya · Vendiendo desde 2011
WhatsApp 998 430 9472 · ventas.altavida@gmail.com
Aparta tu cita de compra (con asesoría financiera de regalo): https://MI-LIGA.vercel.app/?origen=correo
```

### Texto junto al código QR impreso
```
ESCANEA Y APARTA TU CITA DE COMPRA
Propiedades en Cancún y Riviera Maya desde $2.5 millones.
De regalo: asesoría financiera y pre-evaluación de tu crédito.
```
(El QR apunta a `https://MI-LIGA.vercel.app/?origen=qr`)

### Mensaje para grupos donde ya estás
```
Buen día a todos. Esta semana tenemos varias propiedades en zonas de alta plusvalía de Cancún, desde $2.5 millones.
Si alguien está pensando en invertir o cambiarse de casa, aquí puede elegir día y hora para verlas, sin compromiso. Incluye una pre-evaluación de crédito hipotecario sin costo:
https://MI-LIGA.vercel.app/?origen=grupo
```

---

## 3. Los tres mensajes que hacen que sí lleguen

### Al apartar (en cuanto te llega el código)
```
¡Hola [Nombre]! Ya quedó tu cita de compra para el [día] a las [hora]. 🙌
[Si es presencial:] Nos vemos en [dirección de la propiedad]. Te mando la ubicación un día antes.
[Si es videollamada:] Aquí está tu liga: [liga]
Cualquier duda, por aquí estoy. — Jaime, Alta Vida Inmuebles
```

### Un día antes
```
¡Hola [Nombre]! Mañana a las [hora] es tu cita de compra en [lugar].
Contéstame SÍ para confirmarte.
```

### El día que no llegó
```
Hola [Nombre], hoy no coincidimos, no pasa nada.
La propiedad sigue disponible por ahora. ¿Te late reagendar? Elige otro horario aquí: https://MI-LIGA.vercel.app/?origen=reagenda
```

---

## 4. Secuencia de 7 días después de la cita (si no ha respondido)

Siguiente paso de tu proceso: **recoger el apartado**.

| Día | Mensaje |
| --- | --- |
| 1 | `[Nombre], gracias por tu tiempo ayer. Te dejo el resumen de [propiedad]: precio [$], forma de pago [recursos propios/crédito]. ¿Qué te pareció?` |
| 2 | `Te comparto las fotos y la ubicación de [propiedad] para que la veas con tu familia. 📍 [liga]` |
| 3 | `¿Ya revisaste tu pre-evaluación de crédito? Con el apartado de [$] la separamos mientras avanza tu trámite.` |
| 4 | `Te cuento algo: tenemos [número] personas viendo propiedades en esa zona esta semana. Si [propiedad] es la tuya, conviene apartarla.` *(mándalo solo si es verdad)* |
| 5 | `¿Te queda alguna duda sobre la zona, el crédito o la notaría? Te la resuelvo en una llamada de 10 minutos.` |
| 6 | `Si [propiedad] no te convenció, dime qué cambiarías y te mando 2 opciones que sí encajen.` |
| 7 | `[Nombre], cierro tu expediente esta semana para no saturarte. Si quieres retomarlo, aquí sigo. Un abrazo.` |

---

## 5. Tu hoja de Google (para tener todas las citas en un solo lugar)

Ya existe en tu Drive: **"Citas Alta Vida Inmuebles"**, con los encabezados puestos.

Para que se llene sola, la forma recomendada es **Make**, que ya usas:

1. Entra a make.com → **Create a new scenario**.
2. Primer módulo: **Webhooks → Custom webhook** → *Add* → nómbralo "Citas Alta Vida" → copia la dirección que te da (empieza con `https://hook.`).
3. Segundo módulo: **Google Sheets → Add a row** → elige la hoja "Citas Alta Vida Inmuebles".
4. Relaciona las columnas: Día y hora = `cita.inicio`, Nombre = `cita.nombre`, WhatsApp = `cita.whatsapp`, Modalidad = `cita.modalidad`, Correo = `cita.correo`, A qué se dedica = `cita.negocio`, Qué busca = `cita.reto`, Llegó por = `cita.origen`, Código = `cita.id`, Duración = `cita.duracionMinutos`, Fecha de registro = `now`.
5. Activa el escenario (**ON**) y mándame la dirección del paso 2. La pongo en `integraciones.webhookUrl` y hacemos una cita de prueba.

Dos avisos:
- **Esa dirección no lleva contraseñas.** Cualquiera que la vea podría mandarle datos, así que no la compartas.
- **Si Make se cae, la cita igual queda guardada.** Te sigue llegando por WhatsApp con su código: la hoja es un extra, no el corazón del sistema.

> ¿Por qué no Google Apps Script directo? Google no acepta el aviso que manda la página desde el celular del cliente (lo bloquea por seguridad del navegador). Make normalmente sí lo recibe; lo confirmamos con la cita de prueba del paso 5.
