(function(){
Template.__checkName("truncate");
Template["truncate"] = new Template("Template.truncate", (function() {
  var view = this;
  return [ HTML.Raw("<!-- Page heading -->\n    "), Blaze._TemplateWith(function() {
    return {
      title: Spacebars.call("Truncate string"),
      category: Spacebars.call("Miscellaneous")
    };
  }, function() {
    return Spacebars.include(view.lookupTemplate("pageHeading"));
  }), HTML.Raw('\n\n    <div class="wrapper wrapper-content  animated fadeInRight">\n        <div class="row">\n            <div class="col-lg-12">\n                <div class="ibox ">\n                    <div class="ibox-title">\n                        <h5>Truncate string - dotdotdot</h5>\n                    </div>\n\n                    <div class="ibox-content">\n\n                        <p>\n                            A jQuery plugin for advanced cross-browser ellipsis on multiple line content.\n                        </p>\n                    </div>\n                </div>\n            </div>\n        </div>\n        <div class="row">\n            <div class="col-md-6">\n                <div class="ibox ">\n                    <div class="ibox-title">\n                        <h5>Example container with fixed height</h5>\n                    </div>\n                    <div class="ibox-content fh-200">\n\n                        <p class="font-bold  alert alert-warning m-b-sm">\n                            This container has fixed height with 200px. Text overflow the container.\n                        </p>\n                        <p>\n                            Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.\n                            Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.\n                        </p>\n                    </div>\n                </div>\n            </div>\n            <div class="col-md-6">\n                <div class="ibox ">\n                    <div class="ibox-title">\n                        <h5>Example container with fixed height</h5>\n                    </div>\n                    <div class="ibox-content truncate fh-200">\n\n                        <p class="font-bold  alert alert-success m-b-sm">\n                            This container has fixed height with 200px and truncate feature that prevent form overflow the text.\n                        </p>\n                        <p>\n                            Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.\n                            Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.\n                        </p>\n                    </div>\n                </div>\n            </div>\n        </div>\n        <div class="row">\n            <div class="col-md-6">\n                <div class="ibox ">\n                    <div class="ibox-title">\n                        <h5>Custom ellipsis</h5>\n                    </div>\n                    <div class="ibox-content truncate1 fh-150">\n\n                        <p class="font-bold">\n                            You can also change the ellipsis\n                        </p>\n                        <p>\n                            Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.\n                            Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.\n                        </p>\n                    </div>\n                </div>\n            </div>\n            <div class="col-md-6">\n                <div class="ibox ">\n                    <div class="ibox-title">\n                        <h5>You can also choose how to cut off the text</h5>\n                    </div>\n                    <div class="ibox-content truncate2 fh-150">\n\n                        <p class="font-bold">\n                            Example with letter cut off\n                        </p>\n                        <p>\n                            Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.\n                            Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.\n                        </p>\n                    </div>\n                </div>\n            </div>\n        </div>\n    </div>') ];
}));

}).call(this);