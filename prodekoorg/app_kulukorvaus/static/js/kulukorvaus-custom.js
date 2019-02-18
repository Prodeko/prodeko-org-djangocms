$(document).ready(function () {

  var csrftoken = $("[name=csrfmiddlewaretoken]").val();
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });


  var formKulukorvaus = $("#form_kulukorvaus");
  formKulukorvaus.on("submit", function (e) {
    e.preventDefault();
    formData = new FormData((formKulukorvaus).get(0));

    $.ajax({
      url: "",
      type: "POST",
      data: formData,
      contentType: false, // Indicates 'multipart/form-data'
      processData: false,
      success: function (data) {
        // Google Analytics form submission tracking
        dataLayer.push({'event' : 'formSubmitted', 'formName' : 'form_kulukorvaus'});
        document.write(data);
      },

      // Re-renders the same page with error texts.
      error: function (xhr, errmsg, err) {
        if (xhr.status === 500) {
          dataLayer.push({'event' : 'formError', 'formName' : 'form_kulukorvaus'});
          $("#form_kulukorvaus").replaceWith(xhr.responseText);
        } else if (xhr.status === 599) {
          // Google Analytics form error tracking
          dataLayer.push({'event' : 'formError', 'formName' : 'form_kulukorvaus'});
          $("#forms-wrapper").replaceWith(xhr.responseText);
          new Formset(document.querySelector('#form_kulukorvaus'));
          handleFileUploads();
        }
      }
    });
  });

  function handleFileUploads() {
    var arr = [].slice.call(document.querySelectorAll('[type*=file]'));
    arr.shift(); // Remove first element in the array which is the management form input button

    arr.forEach(function (el) {
      el.addEventListener('change', showFileName)
    });
  }

  function removeReceiptName(e) {
    e.target.parentElement.previousElementSibling.value = "";
    $(e.target.parentElement).remove();
  }

  function showFileName(e) {
    var input = e.srcElement;
    var filename = input.files[0].name;

    var span = document.createElement("span");
    span.classList.add("form-text", "receipt-name", "pr-2");
    span.innerHTML = `<i id="removeReceptIcon" class="fas fa-minus-square fa-lg pr-2";"></i> ${filename}`;
    span.firstElementChild.addEventListener("click", removeReceiptName);

    parent = input.parentNode;
    if (parent.children.length > 2) {
      parent.removeChild(parent.children[2]);
    }
    parent.appendChild(span);
  }

  // Add event listeners to receipt upload buttons
  handleFileUploads();

  function Formset(element) {
    /*
  	Dynamic Formset handler for Django formsets.
    Credits: http://schinckel.net/2017/02/05/django-dynamic-formsets/

    Events:

      * init.formset
      * add-form.formset
      * remove-form.formset
      * renumber-form.formset

    */
    if (!(this instanceof Formset)) {
      return new Formset(element);
    }
    var formset = this;
    var emptyForm = element.querySelector('.empty-form').firstElementChild;
    var formsList = element.querySelector('.forms');

    var initialForms = element.querySelector('[name$=INITIAL_FORMS]');
    var totalForms = element.querySelector('[name$=TOTAL_FORMS]');
    var prefix = initialForms.name.replace(/INITIAL_FORMS$/, '');

    function addForm(event) {
      // Duplicate empty form.
      var newForm = emptyForm.cloneNode(true);
      // Update all references to __prefix__ in the elements names.
      renumberForm(newForm, '__prefix__', totalForms.value);
      // Make it able to delete itself.
      newForm.querySelector('[data-formset-remove-form]').addEventListener('click', removeForm);
      // Append the new form to the formsList.
      formsList.insertAdjacentElement('beforeend', newForm);
      // Update the totalForms.value
      totalForms.value = Number(totalForms.value) + 1;
      handleFileUploads();
    }

    function getForm(target) {
      var parent = target.parentElement;
      if (parent == document) {
        return null;
      }
      if (parent == formsList) {
        return target;
      }
      return getForm(parent);
    }

    function renumberForm(form, oldValue, newValue) {
      var matchValue = prefix + oldValue.toString();
      var match = new RegExp(matchValue);
      var replace = prefix + newValue.toString();

      ['name', 'id', 'for'].forEach(function (attr) {
        form.querySelectorAll('[' + attr + '*=' + matchValue + ']').forEach(function (el) {
          el.setAttribute(attr, el.getAttribute(attr).replace(match, replace));
        });
      });
    }

    function removeForm(event) {
      // Find the form "row": the child of formsList that is the parent of the element
      // that triggered this event.
      var formToRemove = getForm(event.target);
      // Renumber the rows that come after us.
      var nextElement = formToRemove.nextElementSibling;
      var nextElementIndex = Array.prototype.indexOf.call(formsList.children, formToRemove);
      while (nextElement) {
        renumberForm(nextElement, nextElementIndex + 1, nextElementIndex);
        nextElement = nextElement.nextElementSibling;
        nextElementIndex = nextElementIndex + 1;
      }
      // Remove this row.
      formToRemove.remove();
      // Decrement the management form's count.
      totalForms.value = Number(totalForms.value) - 1;
      handleFileUploads();
    }

    element.querySelector('[data-formset-add-form]').addEventListener('click', addForm);
    element.formset = this;

    this.addForm = addForm;
  }

  new Formset(document.querySelector('#form_kulukorvaus'));
});