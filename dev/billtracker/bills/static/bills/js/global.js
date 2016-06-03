/* -------------- nav click functionality ------------------- */

$('.navbar-collapse a').click(function(e){

	var clickedLink = $(this);
	var clickedLi = clickedLink.parent();
	var lis = $('.navbar-collapse li');

	var searchTerm = clickedLink.text().toLowerCase();
	console.log('run ajax for ' + searchTerm + ' here.');
	lis.removeClass('active');
	clickedLi.addClass('active');

	e.preventDefault();

    switch (searchTerm) {
        case "content": window.location = "/bills";
             break;
        case "subject": window.location = "/subjects";
             break;
        case "author": window.location = "/authors";
             break;
        default: break;
    }


});







/* -------------- search functionality ------------------- */







/* -------------- single bill view functionality ------------------- */

var lastClicked;

function toggleForm(sentence)
{
	var submissionForm = document.getElementById("submission");

	if (submissionForm.style.visibility != "visible")
	{
		submissionForm.style.visibility = "visible";
		sentence.style.backgroundColor = "yellow";
		lastClicked = sentence;
	}
	else
	{
		submissionForm.style.visibility = "hidden";
		lastClicked.style.backgroundColor = "inherit";
	}
}

function submitAnnotation(text)
{
	var annotationText = text.value;
	var submissionForm = document.getElementById("submission");

	submissionForm.style.visibility = "hidden";
	lastClicked.style.backgroundColor = "inherit";
	alert(annotationText + " submitted as annotation for sentence " +
		lastClicked.id + ".");
	text.value = "";

}




/* ------------------- setup annotation right sidebar --------------- */

if ( $('.billarea').length ) {


	// init vars for annotation y pos calculations
	var annotations = [];
	// about half of highlight height
	// (this gets top of annotation to top of highlight)
	var offset = 7;
	var basePos = $('.billarea').offset().top;

}


function arrangeAnnotations() {

	// move sidebar annotations into bootstrap column
	var sidebar = $('.annotations-list-uoc').detach();
	$('#submission').append(sidebar);

	// give sidebar height (it's contents are absolute so it has none)
	var billAreaHeight = $('.billarea').height();
	$('#submission').css('height',billAreaHeight + 'px');

	// annotation y position calculations - makes sure annotations don't overlap
	$('.annotator-wrapper .annotator-hl').each(function(index){

		var highlight = $(this);
		// var highlightId = highlight.attr('data-annotation-id');
		var highlightId = highlight.attr('class').split(' ')[0].trim();

		// placeAnnotation(index, highlight, highlightId, true);

		var highlightPos = highlight.offset().top;
		var annotationSelector = '#submission #annotation-' + highlightId;
		var highlightTop = highlightPos - basePos - offset;
		var annotationHeight = $(annotationSelector).height();

		loadAnnotation(index,highlightId,highlightTop,annotationHeight);

	});

}




// this is a custom tweak to the annotator.js library.
// it's called from /static/annotatorjs/src/view_annotator.js line 231
// when an annotation is created
function placeNewAnnotation (newAnnotation) {

	// first grab the newest highlight
	var newHighlights = $('.undefined.annotator-hl');

	if (newHighlights.length > 1) {
		function compare(a,b) {
		  if ( parseInt($(a).attr('id')) < parseInt($(b).attr('id')))
		    return -1;
		  if ( parseInt($(a).attr('id')) > parseInt($(b).attr('id')))
		    return 1;
		  return 0;
		}
		newHighlights.sort(compare);
		var highlight = $(newHighlights[newHighlights.length - 1]);
	} else {
		var highlight = newHighlights;
	}

	var annotationTop = null;
	var highlightId = highlight.attr('id');
	var index = $('li.annotator-marginviewer-element').length - 1;
	var highlightPos = highlight.offset().top;
	var annotationSelector = '#submission #annotation-' + highlightId;
	// var highlightTop = highlightPos - basePos - offset;
	var highlightTop = highlight[0].offsetTop + offset * 1.5;
	var annotationHeight = $(annotationSelector).height();
	var isCollision = false;
	var targetTop = highlightTop;
	var targetBot = highlightTop + annotationHeight;

	// console.log('highlightPos: ' + highlightPos);
	// console.log('basePos: ' + basePos);
	// console.log('offset: ' + offset);
	// console.log('highlightPos - basePos - offset: ' + targetTop);


	testAnnotationCollision();

	function testAnnotationCollision() {
		for (var i=0; i<annotations.length; i++) {

			if (!isCollision) {
				var testAnnotation = annotations[i];
				var testTop = testAnnotation.topY;
				var testBot = testAnnotation.botY;

				if ( (targetTop >= testTop) && (targetTop <= testBot) ||
					(targetBot >= testTop) && (targetBot <= testBot) ) {

					isCollision = true;
					targetTop = testBot + offset;
					targetBot = targetTop + annotationHeight;

				}
			}

		}

		if (!isCollision) {

			annotationTop = targetTop;

		} else {

			isCollision = false;
			testAnnotationCollision();

		}

	}

	// console.log('annotationTop: ' + annotationTop);
	$('#submission #annotation-' + highlightId).css('top', annotationTop + 'px');

	annotations.push({
		id: highlightId,
		highlightY: highlightTop,
		annotationHeight: annotationHeight,
		topY: annotationTop,
		botY: annotationTop + annotationHeight
	});


}




function loadAnnotation(index,highlightId,highlightTop,annotationHeight) {

	var annotationTop = null;

	if (index==0) {

		annotationTop = highlightTop + offset;

	} else {

		var prevIndex = index - 1;
		var prevAnnotation = annotations[prevIndex];
		var targetTop = highlightTop;
		var targetBot = highlightTop + annotationHeight;
		var prevTop = prevAnnotation.topY;
		var prevBot = prevAnnotation.botY;

		// console.log(annotations.length);

		// there's a bug here
		// this only checks against last annotation placed, not all already placed
		// hence https://github.com/bill-tracker/bill-tracker/issues/171

		var isCollision	= false;

		testAnnotationCollision();

		function testAnnotationCollision() {
			for (var i=0; i<annotations.length; i++) {

				if (!isCollision) {
					var testAnnotation = annotations[i];
					var testTop = testAnnotation.topY;
					var testBot = testAnnotation.botY;

					if ( (targetTop >= testTop) && (targetTop <= testBot) ||
						(targetBot >= testTop) && (targetBot <= testBot) ) {

						isCollision = true;
						targetTop = testBot + offset;
						targetBot = targetTop + annotationHeight;

					}
				}

			}

			if (!isCollision) {

				annotationTop = targetTop + offset;

			} else {

				isCollision = false;
				testAnnotationCollision();

			}

		}


		// if ( (targetTop > prevTop) && (targetTop < prevBot) ||
		// 	(targetBot > prevTop) && (targetBot < prevBot) ) {
		// 	annotationTop = prevBot + 15;
		// } else {
		// 	annotationTop = targetTop + offset;
		// }

	}

	$('#submission #annotation-' + highlightId).css('top', annotationTop + 'px');

	annotations.push({
		id: highlightId,
		highlightY: highlightTop,
		annotationHeight: annotationHeight,
		topY: annotationTop,
		botY: annotationTop + annotationHeight
	});

}


/* ------------ contact form validation -------------- */

/* from http://codepen.io/jaycbrf/pen/iBszr */
$(document).ready(function() {
	$('#contact_form').bootstrapValidator({
	// To use feedback icons, ensure that you use Bootstrap v3.1.0 or later
	feedbackIcons: {
	    valid: 'fa fa-check',
	    invalid: 'fa fa-close',
	    validating: 'fa fa-refresh'
	},
	fields: {
	    first_name: {
	        validators: {
	                stringLength: {
	                min: 2,
	            },
	                notEmpty: {
	                message: 'Please supply your first name'
	            }
	        }
	    },
	     last_name: {
	        validators: {
	             stringLength: {
	                min: 2,
	            },
	            notEmpty: {
	                message: 'Please supply your last name'
	            }
	        }
	    },
	    email: {
	        validators: {
	            notEmpty: {
	                message: 'Please supply your email address'
	            },
	            emailAddress: {
	                message: 'Please supply a valid email address'
	            }
	        }
	    },
	    phone: {
	        validators: {
	            notEmpty: {
	                message: 'Please supply your phone number'
	            },
	            phone: {
	                country: 'US',
	                message: 'Please supply a vaild phone number with area code'
	            }
	        }
	    },
	    address: {
	        validators: {
	             stringLength: {
	                min: 8,
	            },
	            notEmpty: {
	                message: 'Please supply your street address'
	            }
	        }
	    },
	    city: {
	        validators: {
	             stringLength: {
	                min: 4,
	            },
	            notEmpty: {
	                message: 'Please supply your city'
	            }
	        }
	    },
	    state: {
	        validators: {
	            notEmpty: {
	                message: 'Please select your state'
	            }
	        }
	    },
	    zip: {
	        validators: {
	            notEmpty: {
	                message: 'Please supply your zip code'
	            },
	            zipCode: {
	                country: 'US',
	                message: 'Please supply a vaild zip code'
	            }
	        }
	    },
	    comment: {
	        validators: {
	              stringLength: {
	                min: 10,
	                max: 200,
	                message:'Please enter at least 10 characters and no more than 200'
	            },
	            notEmpty: {
	                message: 'Please supply a description of your project'
	            }
	            }
	        }
	    }
	})
	.on('success.form.bv', function(e) {
	    $('#success_message').slideDown({ opacity: "show" }, "slow") // Do something ...
	        $('#contact_form').data('bootstrapValidator').resetForm();

	    // Prevent form submission
	    e.preventDefault();

	    // Get the form instance
	    var $form = $(e.target);

	    // Get the BootstrapValidator instance
	    var bv = $form.data('bootstrapValidator');

	    // Use Ajax to submit form data
	    $.post($form.attr('action'), $form.serialize(), function(result) {
	        console.log(result);
	    }, 'json');
	});
});



/* ------------ demo functionality -------------- */

/* homepage demo (page 1) */
if ( $('body.home').length) {

	document.getElementById('demo').onclick = function() {

		introJs().start();

		// $('.introjs-nextpagebutton').css('border','1px solid red');

		// introJs().setOption('doneLabel', 'Next page').start().oncomplete(function() {
	  // 	window.location.href = '/demo-bill.html';
		// });

		// introJs().setOption('nextLabel', 'Next page').start().oncomplete(function() {
		// 	console.log('hi');
		// });
	};

}

/* billpage demo (page 2) */

if ( $('.demoBill').length) {

	introJs().start();

	var counter = 0;
	$('a.introjs-button').click(function(){
		counter++;
		if (counter == 1) {
				// console.log('counter: ' + counter);
				$('.annotator-pencil').css('visibility','visible');
		} else if (counter == 2) {
			// console.log('counter: ' + counter);
			$('.annotator-pencil').css('visibility','hidden');
			$('.annotator-original').css('visibility','visible');
		} else if (counter == 3) {
			$('.annotator-original').css('visibility','hidden');
			$('.annotator-marginviewer-element').css('visibility','visible');
		}
	});

	// set the date in the example annotation to today's date & time
	var now = new Date();
	var month = now.getMonth() + 1;
	var day = now.getDate();
	var year = now.getFullYear();
	$('.annotator-marginviewer-date').text(month + '/' + day + '/' + year);

}
