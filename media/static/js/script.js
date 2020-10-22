/*jshint jquery:true */

$(document).ready(function($) {
	"use strict";

	/* global google: false */
	/*jshint -W018 */

	/*-------------------------------------------------*/
	/* =  portfolio isotope
	/*-------------------------------------------------*/

	var winDow = $(window);
		// Needed variables
		var $container=$('.iso-call');
		var $filter=$('.filter');

		try{
			$container.imagesLoaded( function(){
				$container.trigger('resize');
				$container.isotope({
					filter:'*',
					layoutMode:'masonry',
					animationOptions:{
						duration:750,
						easing:'linear'
					}
				});
				setTimeout(Resize, 1500);
			});
		} catch(err) {
		}

		winDow.on('resize', function(){
			var selector = $filter.find('a.active').attr('data-filter');

			try {
				$container.isotope({ 
					filter	: selector,
					animationOptions: {
						duration: 750,
						easing	: 'linear',
						queue	: false,
					}
				});
			} catch(err) {
			}
			return false;
		});
		
		// Isotope Filter 
		$filter.find('a').on('click', function(){
			var selector = $(this).attr('data-filter');

			try {
				$container.isotope({ 
					filter	: selector,
					animationOptions: {
						duration: 750,
						easing	: 'linear',
						queue	: false,
					}
				});
			} catch(err) {

			}
			return false;
		});


	var filterItemA	= $('.filter li a');

		filterItemA.on('click', function(){
			var $this = $(this);
			if ( !$this.hasClass('active')) {
				filterItemA.removeClass('active');
				$this.addClass('active');
			}
		});

	/*-------------------------------------------------*/
	/* =  Search animation
	/*-------------------------------------------------*/
	
	var searchToggle = $('.open-search'),
		inputAnime = $(".form-search"),
		body = $('body');

	searchToggle.on('click', function(event){
		event.preventDefault();

		if ( !inputAnime.hasClass('active') ) {
			inputAnime.addClass('active');
		} else {
			inputAnime.removeClass('active');			
		}
	});

	body.on('click', function(){
		inputAnime.removeClass('active');
	});

	var elemBinds = $('.open-search, .form-search');
	elemBinds.on('click', function(e) {
		e.stopPropagation();
	});

	/*-------------------------------------------------*/
	/* =  nav animate app home page
	/*-------------------------------------------------*/

	var openCloseButton = $('a.open-close-menu'),
		ToogleHeader = $('.toogle-menu');

	openCloseButton.on('click', function(event) {
		event.preventDefault();
		ToogleHeader.toggleClass('active');
	});

	/*-------------------------------------------------*/
	/* =  fixed right sidebar animate
	/*-------------------------------------------------*/

	var openRightSidebar = $('a.open-fixed-sidebar'),
		closeRightSidebar = $('a.close-fixed-sidebar'),
		rightSidebar = $('#fixed-sidebar');

	openRightSidebar.on('click', function(event) {
		event.preventDefault();
		if (!rightSidebar.hasClass('active')) {
			rightSidebar.addClass('active');
		} else {
			rightSidebar.removeClass('active');
		}
	});

	closeRightSidebar.on('click', function(event) {
		event.preventDefault();
		rightSidebar.removeClass('active');
	});

	/*-------------------------------------------------*/
	/* =  nav animate
	/*-------------------------------------------------*/

	var ToogleMenu = $('li.open-menu a');

	ToogleMenu.on('click', function(event) {
		event.preventDefault();

		var MainMenu = $('.navbar-nav'),
			$this = $(this);
		if ( !$this.hasClass('opened') ) {
			$this.addClass('opened');
			MainMenu.addClass('active');
		} else {
			$this.removeClass('opened');
			MainMenu.removeClass('active');
		}
	});

	/*-------------------------------------------------*/
	/* =  news accord
	/*-------------------------------------------------*/

	var newsLink = $('a.title-link');

		newsLink.on('click', function(event){
			event.preventDefault();
			var HisParent = $(this).parents('.blog-post, .menu-post');
			console.log(HisParent);
			if( !HisParent.hasClass('active') ) {

				$('.blog-post .content-box, .menu-post .content-box').slideUp(300, function(){
					$('.blog-post, .menu-post').removeClass('active');
				});

				HisParent.find('.content-box').slideDown(300, function(){
					HisParent.addClass('active');
				});
			} else {
				$('.blog-post.active .content-box, .menu-post.active .content-box').slideUp(300, function(){
					HisParent.removeClass('active');
				});
			}

		});

	/*-------------------------------------------------*/
	/* =  about tabs
	/*-------------------------------------------------*/

	var tabLinK = $('.about-post a'),
		tabContenT = $('.tab-cont');

		tabLinK.on('click', function(event){
			event.preventDefault();
			var dataLink = $(this).attr('data-link'),
				dataTab = $('.tab-cont.active').attr('data-tab');

			if(!$(this).hasClass('active')) {
				$('.about-post a').removeClass('active');
				$(this).addClass('active');
			}

			if ( dataLink == dataTab ) {
			} else {
				tabContenT.removeClass('active');
				$('.tab-cont[data-tab='+ dataLink +']').addClass('active');
			}
		});

	/*-------------------------------------------------*/
	/* =  OWL carousell
	/*-------------------------------------------------*/
	try {
		var owlWrap = $('.owl-wrapper');

		if (owlWrap.length > 0) {

			if (jQuery().owlCarousel) {
				owlWrap.each(function(){

					var carousel= $(this).find('.owl-carousel'),
						dataNum = $(this).find('.owl-carousel').attr('data-num'),
						dataNum2,
						dataNum3;

					if ( dataNum == 1 ) {
						dataNum2 = 1;
						dataNum3 = 1;
					} else if ( dataNum == 2 ) {
						dataNum2 = 2;
						dataNum3 = dataNum - 1;
					} else {
						dataNum2 = dataNum - 1;
						dataNum3 = dataNum - 2;
					}

					carousel.owlCarousel({
						autoPlay: 10000,
						navigation : true,
						items : dataNum,
						itemsDesktop : [1199,dataNum2],
						itemsDesktopSmall : [979,dataNum3],
						itemsTablet : [768, dataNum3],
					});

				});
			}
		}

	} catch(err) {

	}
	
	/*-------------------------------------------------*/
	/* =  comming soon & error height fix
	/*-------------------------------------------------*/
	
	$('.error-section, .comming-soon-section').css('min-height', $(window).height() - $('.navbar-default').height());

	try {

		$('#clock').countdown("2020/01/29", function(event) {
			var $this = $(this);
			switch(event.type) {
				case "seconds":
				case "minutes":
				case "hours":
				case "days":
				case "daysLeft":
					$this.find('span#'+event.type).html(event.value);
					break;
				case "finished":
					$this.hide();
					break;
			}
		});

	} catch(err) {

	}

	/* ---------------------------------------------------------------------- */
	/*	Accordion
	/* ---------------------------------------------------------------------- */
	var clickElem = $('a.accord-link');

	clickElem.on('click', function(e){
		e.preventDefault();

		var $this = $(this),
			parentCheck = $this.parents('.accord-elem'),
			accordItems = $('.accord-elem'),
			accordContent = $('.accord-content');
			
		if( !parentCheck.hasClass('active')) {

			accordContent.slideUp(400, function(){
				accordItems.removeClass('active');
			});
			parentCheck.find('.accord-content').slideDown(400, function(){
				parentCheck.addClass('active');
			});

		} else {

			accordContent.slideUp(400, function(){
				accordItems.removeClass('active');
			});

		}
	});

	/*-------------------------------------------------*/
	/* =  flexslider
	/*-------------------------------------------------*/

	try {

		var SliderPost = $('.flexslider');

		SliderPost.flexslider({
			slideshowSpeed: 3000,
			easing: "swing"
		});
	} catch(err) {

	}
	
	/* ---------------------------------------------------------------------- */
	/*	Contact Map
	/* ---------------------------------------------------------------------- */
	var contact = {"lat":"37.7867696", "lon":"-122.3894395"}; //Change a map coordinate here!

	try {
		var mapContainer = $('.map');
		mapContainer.gmap3({
			action: 'addMarker',
			marker:{
				options:{
					icon : new google.maps.MarkerImage('images/marker.png')
				}
			},
			latLng: [contact.lat, contact.lon],
			map:{
				center: [contact.lat, contact.lon],
				zoom: 14
				},
			},
			{action: 'setOptions', args:[{scrollwheel:false}]}
		);
	} catch(err) {

	}
	
	/*-------------------------------------------------*/
	/* =  Scroll to TOP
	/*-------------------------------------------------*/

	var animateTopButton = $('.go-top'),
		htmBody = $('html, body');
		
	animateTopButton.on('click', function(){
	htmBody.animate({scrollTop: 0}, 'slow');
		return false;
	});

	/* ---------------------------------------------------------------------- */
	/*	magnific-popup
	/* ---------------------------------------------------------------------- */

	try {
		// Example with multiple objects
		$('.zoom').magnificPopup({
			type: 'image',
			gallery: {
				enabled: true
			}
		});

	} catch(err) {

	}
	
	/*-------------------------------------------------*/
	/* = slider Testimonial
	/*-------------------------------------------------*/

	var slidertestimonial = $('.bxslider');
	
	try{		
		slidertestimonial.bxSlider({
			mode: 'vertical',
			pagerCustom: '#bx-pager'
		});

		$('.slider-call').bxSlider({
			pagerCustom: '#bx-pager'
		});

		$('.bxslider-posts, .bxslider-test').bxSlider();

	} catch(err) {
	}

	/*-------------------------------------------------*/
	/* =  count increment
	/*-------------------------------------------------*/
	try {
		$('.statistic-post').appear(function() {
			$('.timer').countTo({
				speed: 4000,
				refreshInterval: 60,
				formatter: function (value, options) {
					return value.toFixed(options.decimals);
				}
			});
		});
	} catch(err) {

	}

	/* ---------------------------------------------------------------------- */
	/*	Shop galery image replacement
	/* ---------------------------------------------------------------------- */

	var elemToShow = $('.other-products a');

	elemToShow.on('click', function(e){
		e.preventDefault();
		var newImg = $(this).attr('data-image');
		var prodHolder = $('.image-holder img');
		prodHolder.attr('src', newImg);
	});

	/*-------------------------------------------------*/
	/* =  shopping cart subtotals, product increase, 
	/* =  decrease, delete item, dropdown remove item from 
	/* =  shopping cart
	/*-------------------------------------------------*/
	
	var totalPrice = $('.total-price');
	var ShippingPrice = $('.shipping-price').text();
	var PriceAfterShipping = $('.total-price-withshipping');

	PriceSum();

	function PriceSum() {

		var sum = 0;

		$('.tot-price').each(function(){
			sum += parseFloat($(this).text());
		});

		totalPrice.text(parseFloat(sum, 10).toFixed(2));

		if ($.isNumeric(ShippingPrice)) {
			PriceAfterShipping.text(parseFloat(parseFloat(sum, 10) + parseFloat(ShippingPrice, 10), 10).toFixed(2));
		} else {
			PriceAfterShipping.text(parseFloat(sum, 10).toFixed(2));
		}
	}


	var btnIncrease = $('button.increase'),
		btnDecrease = $('button.decrease'),
		DeleteButton = $('a.remove-item');

		btnIncrease.on('click', function(){
			var fieldNum = $(this).parent('.quantity-add').find('input[type="text"]');
			var fieldVal = fieldNum.val();
			var nextVal = parseFloat(fieldVal) + 1;
			fieldNum.val(nextVal);
			var itemPrice = $(this).parents('tr').find('span.stat-price').text();
			var totPrice = $(this).parents('tr').find('span.tot-price');
			var newPrice = parseFloat(parseFloat(itemPrice, 10) * parseFloat(fieldNum.val(), 10), 10).toFixed(2);
			totPrice.text(newPrice);

			PriceSum();
		});

		btnDecrease.on('click', function(){
			var fieldNum = $(this).parent('.quantity-add').find('input[type="text"]');
			var fieldVal = fieldNum.val();
			var nextVal = parseFloat(fieldVal) - 1;
			if (fieldVal > 0) {
				fieldNum.val(nextVal);
				var itemPrice = $(this).parents('tr').find('span.stat-price').text();
				var totPrice = $(this).parents('tr').find('span.tot-price');
				var newPrice = parseFloat(parseFloat(itemPrice, 10) * parseFloat(fieldNum.val(), 10), 10).toFixed(2);
				totPrice.text(newPrice);
			} else {
				fieldNum.val(0);
			}

			PriceSum();
		});

		DeleteButton.on('click', function(event) {
			event.preventDefault();

			$(this).closest('tr').remove();

			PriceSum();
		});

	var removeItemShop = $('a.delete-art');

	removeItemShop.on('click', function(event) {
		event.preventDefault();
		$(this).closest('li').remove();
	});
	/* ---------------------------------------------------------------------- */
	/*	Contact Form
	/* ---------------------------------------------------------------------- */

	var submitContact = $('#submit_contact'),
		message = $('#msg');

	submitContact.on('click', function(e){
		e.preventDefault();

		var $this = $(this);
		
		$.ajax({
			type: "POST",
			url: 'contact.php',
			dataType: 'json',
			cache: false,
			data: $('#contact-form').serialize(),
			success: function(data) {

				if(data.info !== 'error'){
					$this.parents('form').find('input[type=text],textarea,select').filter(':visible').val('');
					message.hide().removeClass('alert-success').removeClass('alert-danger').addClass('alert-success').html(data.msg).fadeIn('slow').delay(5000).fadeOut('slow');
				} else {
					message.hide().removeClass('alert-success').removeClass('alert-danger').addClass('alert-danger').html(data.msg).fadeIn('slow').delay(5000).fadeOut('slow');
				}
			}
		});
	});

	/* ---------------------------------------------------------------------- */
	/*	Load more posts from container
	/* ---------------------------------------------------------------------- */

	var LoadButton = $('a.load-post-container'),
		PortContainer = ('.iso-call'),
		i = 0,
		s = 0;

	LoadButton.on( 'click', function(event) {
		event.preventDefault();

		var LoadContainer = $(this).attr('data-load'),
			xel = parseInt($(this).attr('data-number'), 10);

		var storage = document.createElement('div');
		$(storage).load("load-container/" + LoadContainer + " .project-post, .blog-post", function(){

			var elemloadedLength = $(storage).find('.project-post, .blog-post').length;
			
			if ( !((s + 1) > elemloadedLength) ) {

				s = i + xel;

				var t = i - 1;
				var $elems;

				if ( i === 0 ) {
					/// create new item elements
					$elems = $(storage).find(".project-post:lt(" + s + "), .blog-post:lt(" + s + ")").appendTo(PortContainer);
					// append elements to container
					$container.isotope( 'appended', $elems );
					recallMagnific();

					if ( LoadContainer == "blog-container3.html") {
						$(storage).find(".blog-post:lt(" + s + ")").appendTo('.blog-box.timeline');
					}

				} else {
					/// create new item elements
					$elems = $(storage).find(".project-post:lt(" + s + "):gt("+ t +"), .blog-post:lt(" + s + "):gt("+ t +")").appendTo(PortContainer);
					// append elements to container
					$container.isotope( 'appended', $elems );
					recallMagnific();

					if ( LoadContainer == "blog-container3.html") {
						$(storage).find(".blog-post:lt(" + s + "):gt("+ t +")").appendTo('.blog-box.timeline');
					}
				}

				i = i + xel;
			}

			if ( !( s < elemloadedLength ) ) {
				$('a.load-post-container').text("No more posts");
			}

		});
	
	});

	/*-------------------------------------------------*/
	/* =  price range code
	/*-------------------------------------------------*/

	try {

		for( var xy = 100; xy <= 10000; xy++ ){
			$('#start-val').append(
				'<option value="' + xy + '">' + xy + '</option>'
			);
		}
		// Initialise noUiSlider
		$('.noUiSlider').noUiSlider({
			range: [0,280],
			start: [0,230],
			handles: 2,
			connect: true,
			step: 1,
			serialization: {
				to: [ $('#start-val'),
					$('#end-val') ],
				resolution: 1
			}
		});
	} catch(err) {

	}

	/* ---------------------------------------------------------------------- */
	/*	menu responsive
	/* ---------------------------------------------------------------------- */
	var menuClick = $('a.elemadded'),
		navbarVertical = $('.menu');
		
	menuClick.on('click', function(e){
		e.preventDefault();

		if( navbarVertical.hasClass('active') ){
			navbarVertical.slideUp(300).removeClass('active');
		} else {
			navbarVertical.slideDown(300).addClass('active');
		}
	});

	winDow.on('resize', function(){
		if ( winDow.width() > 991 ) {
			navbarVertical.slideDown(300).removeClass('active');
		} else {
			navbarVertical.slideUp(300).removeClass('active');
		}
	});

	/* ---------------------------------------------------------------------- */
	/*	Header animate after scroll
	/* ---------------------------------------------------------------------- */

	(function() {

		var docElem = document.documentElement,
			didScroll = false,
			changeHeaderOn = 130;
			document.querySelector( 'header, a.go-top' );
		function init() {
			window.addEventListener( 'scroll', function() {
				if( !didScroll ) {
					didScroll = true;
					setTimeout( scrollPage, 100 );
				}
			}, false );
		}
		
		function scrollPage() {
			var sy = scrollY();
			if ( sy >= changeHeaderOn ) {
				$( 'header' ).addClass('active');
				$( 'a.go-top' ).addClass('active');
			}
			else {
				$( 'header' ).removeClass('active');
				$( 'a.go-top' ).removeClass('active');
			}
			didScroll = false;
		}
		
		function scrollY() {
			return window.pageYOffset || docElem.scrollTop;
		}
		
		init();
		
	})();

});

/* ---------------------------------------------------------------------- */
	/*	magnific-popup function
	/* ---------------------------------------------------------------------- */
function recallMagnific(){
	$('.zoom').magnificPopup({
		type: 'image',
		gallery: {
			enabled: true
		}
	});
}


function Resize() {
	$(window).trigger('resize');
}