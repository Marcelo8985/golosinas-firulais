/* ===========================================================
   Las Golosinas del Firulais — Script principal (jQuery + DOM)
   =========================================================== */
$(document).ready(function () {

  /* 1) Menú hamburguesa responsivo (jQuery + manipulación de clases) */
  $('.menu-toggle').on('click', function () {
    $('nav.navbar ul').toggleClass('abierto');
  });

  /* 2) Marcar automáticamente el link activo según la página actual (DOM) */
  var paginaActual = window.location.pathname.split('/').pop() || 'index.html';
  $('nav.navbar a').each(function () {
    var href = $(this).attr('href');
    if (href === paginaActual) {
      $(this).addClass('activo');
    }
  });

  /* 3) Año dinámico en el pie de página (DOM) */
  var anioActual = new Date().getFullYear();
  $('#anio').text(anioActual);

  /* 4) PRODUCTOS: se cargan desde la base de datos vía GET /api/productos
        (ya no son fijos en el HTML). Se arman las tarjetas y los botones
        de filtro por categoría dinámicamente con jQuery + DOM. */
  if ($('#grid-productos').length) {
    $.ajax({ url: '/api/productos', method: 'GET' })
      .done(function (productos) {
        $('#estado-carga-productos').hide();

        var categorias = [];
        productos.forEach(function (prod) {
          if (categorias.indexOf(prod.nombre_categoria) === -1) categorias.push(prod.nombre_categoria);
        });

        var htmlFiltros = '<button class="filtro-btn activo-filtro" data-categoria="todos">Todos</button>';
        categorias.forEach(function (cat) {
          htmlFiltros += '<button class="filtro-btn" data-categoria="' + cat + '">' + cat + '</button>';
        });
        $('#filtros').html(htmlFiltros);

        var htmlProductos = '';
        productos.forEach(function (prod) {
          htmlProductos += '' +
            '<div class="card" data-categoria="' + prod.nombre_categoria + '">' +
              '<img src="img/' + prod.imagen + '" alt="' + prod.nombre_producto + '">' +
              '<div class="card-body">' +
                '<h4>' + prod.nombre_producto + '</h4>' +
                '<p>' + prod.descripcion + '</p>' +
                '<span class="precio">$' + prod.precio.toFixed(2) + '</span>' +
              '</div>' +
            '</div>';
        });
        $('#grid-productos').html(htmlProductos);
      })
      .fail(function () {
        $('#estado-carga-productos').text('No se pudieron cargar los productos. Verifica que el servidor esté activo.');
      });
  }

  // Filtro de catálogo por categoría (delegado, porque los botones se crean dinámicamente)
  $(document).on('click', '.filtro-btn', function () {
    var categoria = $(this).data('categoria');
    $('.filtro-btn').removeClass('activo-filtro');
    $(this).addClass('activo-filtro');

    if (categoria === 'todos') {
      $('.card[data-categoria]').fadeIn(200);
    } else {
      $('.card[data-categoria]').each(function () {
        if ($(this).data('categoria') === categoria) {
          $(this).fadeIn(200);
        } else {
          $(this).fadeOut(200);
        }
      });
    }
  });

  /* 5) OFERTAS DEL MES: se cargan desde la base de datos vía GET /api/ofertas */
  if ($('#contenedor-ofertas').length) {
    $.ajax({ url: '/api/ofertas', method: 'GET' })
      .done(function (ofertas) {
        $('#estado-carga-oferta').hide();

        if (ofertas.length === 0) {
          $('#contenedor-ofertas').html('<p style="text-align:center;">No hay ofertas activas este mes.</p>');
          return;
        }

        var html = '';
        ofertas.forEach(function (of, indice) {
          var precioFinal = (of.precio * (1 - of.descuento / 100)).toFixed(2);
          html += '' +
            '<div class="oferta-box" style="margin-bottom:24px;">' +
              '<span class="badge">' + of.descuento + '% de descuento</span>' +
              '<img src="img/' + of.imagen + '" alt="' + of.nombre_producto + '" style="border-radius:14px;margin:0 auto 16px;">' +
              '<h4 style="color:var(--marron-oscuro);font-size:1.4rem;">' + of.nombre_producto + '</h4>' +
              '<p style="margin-top:10px;">' + of.descripcion + '</p>' +
              '<p style="margin-top:14px;">' +
                '<span style="text-decoration:line-through;color:#a58a6c;">$' + of.precio.toFixed(2) + '</span>' +
                ' <strong style="color:var(--naranja);font-size:1.3rem;">$' + precioFinal + '</strong>' +
              '</p>' +
              '<div class="contador-oferta" data-fin="' + of.fecha_fin + '" id="contador-' + indice + '"></div>' +
              '<a href="contacto.html" class="btn">Reservar ahora</a>' +
            '</div>';
        });
        $('#contenedor-ofertas').html(html);

        function actualizarContadores() {
          $('.contador-oferta').each(function () {
            var fechaFin = new Date($(this).data('fin') + 'T23:59:59');
            var diff = fechaFin - new Date();
            if (diff <= 0) {
              $(this).text('¡La oferta vence hoy, aprovecha!');
              return;
            }
            var dias = Math.floor(diff / (1000 * 60 * 60 * 24));
            var horas = Math.floor((diff / (1000 * 60 * 60)) % 24);
            $(this).text('Quedan ' + dias + ' días y ' + horas + ' h de oferta');
          });
        }
        actualizarContadores();
        setInterval(actualizarContadores, 60000);
      })
      .fail(function () {
        $('#estado-carga-oferta').text('No se pudieron cargar las ofertas. Verifica que el servidor esté activo.');
      });
  }

  /* 6) NOTICIAS: se cargan desde la base de datos vía GET /api/noticias
        (tabla Noticia: fecha, titulo, contenido, imagen) */
  if ($('#lista-noticias').length) {
    $.ajax({ url: '/api/noticias', method: 'GET' })
      .done(function (noticias) {
        $('#estado-carga-noticias').hide();

        var html = '';
        noticias.forEach(function (n) {
          var fechaLegible = new Date(n.fecha + 'T00:00:00').toLocaleDateString('es-EC', { year: 'numeric', month: 'long', day: 'numeric' });
          html += '' +
            '<div class="noticia-dinamica">' +
              '<img src="img/' + n.imagen + '" alt="' + n.titulo + '">' +
              '<div class="contenido-noticia">' +
                '<div class="fecha">' + fechaLegible + '</div>' +
                '<h4>' + n.titulo + '</h4>' +
                '<p>' + n.contenido + '</p>' +
              '</div>' +
            '</div>';
        });
        $('#lista-noticias').html(html);
      })
      .fail(function () {
        $('#estado-carga-noticias').text('No se pudieron cargar las noticias. Verifica que el servidor esté activo.');
      });
  }

  /* 7) CONTACTO: valida en el cliente y luego GUARDA en la
        base de datos a través de la API Flask (POST /api/contacto).
        El servidor responde con el mensaje de confirmación (acuse de recibido). */
  $('#form-contacto').on('submit', function (e) {
    e.preventDefault();
    var valido = true;

    var nombre = $('#nombre').val().trim();
    var email = $('#email').val().trim();
    var mensaje = $('#mensaje').val().trim();
    var regexEmail = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

    if (nombre === '') {
      $('#error-nombre').text('Por favor ingresa tu nombre.').show();
      valido = false;
    } else {
      $('#error-nombre').hide();
    }

    if (!regexEmail.test(email)) {
      $('#error-email').text('Ingresa un correo electrónico válido.').show();
      valido = false;
    } else {
      $('#error-email').hide();
    }

    if (mensaje === '') {
      $('#error-mensaje').text('Cuéntanos qué necesitas para tu mascota.').show();
      valido = false;
    } else {
      $('#error-mensaje').hide();
    }

    if (!valido) {
      $('#mensaje-exito').hide();
      return;
    }

    var $boton = $('#btn-guardar-contacto');
    $boton.prop('disabled', true).text('Guardando...');

    $.ajax({
      url: '/api/contacto',
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ nombre: nombre, email: email, mensaje: mensaje }),
    }).done(function (respuesta) {
      $('#mensaje-exito').fadeIn(300).text(respuesta.mensaje);
      $('#form-contacto')[0].reset();
    }).fail(function (xhr) {
      var texto = 'Ocurrió un error al guardar tu mensaje. Intenta nuevamente.';
      if (xhr.responseJSON && xhr.responseJSON.errores) {
        texto = Object.values(xhr.responseJSON.errores).join(' ');
      }
      $('#mensaje-exito').hide();
      $('#error-mensaje').text(texto).show();
    }).always(function () {
      $boton.prop('disabled', false).text('Guardar');
    });
  });

  /* 8) Reporteador de Clima: consulta la API Flask (que a su vez consulta
        OpenWeatherMap) y muestra Temperatura, Humedad, Descripción y Viento. */
  $('#btn-consultar-clima').on('click', function () {
    var $boton = $(this);
    $('#clima-error').hide();
    $('#clima-resultado').hide();
    $('#clima-cargando').show();
    $boton.prop('disabled', true);

    $.ajax({ url: '/api/clima', method: 'GET' })
      .done(function (datos) {
        $('#clima-ciudad').text(datos.ciudad);
        $('#clima-temp').text(datos.temperatura + ' °C');
        $('#clima-humedad').text(datos.humedad + ' %');
        $('#clima-descripcion').text(datos.descripcion);
        $('#clima-viento').text(datos.viento + ' m/s');
        $('#clima-resultado').fadeIn(300);
      })
      .fail(function (xhr) {
        var texto = 'No se pudo consultar el clima en este momento.';
        if (xhr.responseJSON && xhr.responseJSON.error) texto = xhr.responseJSON.error;
        $('#clima-error').text(texto).show();
      })
      .always(function () {
        $('#clima-cargando').hide();
        $boton.prop('disabled', false);
      });
  });

});
