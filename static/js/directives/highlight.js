angular.module('angular-highlight', []).directive('highlight', function() {
  var component = function(scope, element, attrs) {

    if (!attrs.highlightClass) {
      attrs.highlightClass = 'angular-highlight';
    }

    var replacer = function(match, item) {
      return '<span class="'+attrs.highlightClass+'">'+match+'</span>';
    };

    var ner_replacer = function(match, item) {
      return '<span class="'+'ner'+'">'+match+'</span>';
    };

    var tokenize = function(keywords) {
      //keywords = keywords.replace(new RegExp(',$','g'), '').split(',');
      if(typeof(keywords) == 'string') keywords = JSON.parse(keywords);
      var i;
      var l = keywords.length;
      for (i=0;i<l;i++) {
        keywords[i] = '\\W'+keywords[i].replace(new RegExp('^ | $','g'), '')+'\\W';
      }
      return keywords;
    };

    scope.$watch('currentDoc', function() {
      var keywords =  attrs['keywords'];
      var text = attrs['text'];

      if (!keywords || keywords == '') {
        element.html(text);
        return false;
      }

      var tokenized	= tokenize(keywords);
      var regex = new RegExp(tokenized.join('|'), 'gmi');

      if (scope.currentDoc.ner) {
        var ner = angular.copy(scope.currentDoc.ner);
        var ner_tokenized = tokenize(ner);
        var ner_regex = new RegExp(ner_tokenized.join('|'), 'gmi');
        var paragraphs = text.split('\n').map(function (s) {
          if (s != '') return '<p>' + s.replace(regex, replacer).replace(ner_regex, ner_replacer) + '</p>';
        });
      } else {
        // Find the words
        var paragraphs = text.split('\n').map(function (s) {
          if (s != '') return '<p>' + s.replace(regex, replacer) + '</p>';
        });
      }

      var html = paragraphs.join('\n');

      element.html(html);
    }, true);
  };
  return {
    restrict: 'EA',
    link: 			component,
    replace:		false,
    scope: true
  };
});
