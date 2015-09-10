SearchApp.directive('dateInput', function (PikadayConfig) {
  // Constants Go Here.
  PikadayConfig = PikadayConfig || {};

  function formatDateView(dateIn) {
    return moment(dateIn).utc().format('L');
  }
  function formatDateModel(dateIn) {
    return moment(dateIn).utc().format('YYYY-MM-DD');
  }

  return {
    scope: {
      'date': '=ngModel',
      'max': '=',
      'min': '='
    },
    require: 'ngModel',
    link: function(scope, element, attrs, ngModelController) {

      var options = {
          field: element[0],
          format: 'YYYY-MM-DD'
      };
      angular.extend(options, PikadayConfig, attrs.pikaday ? scope.$parent.$eval(attrs.pikaday) : {});

      var onSelect = options.onSelect;
      var onOpen = options.onOpen;

      options.onSelect = function(date) {
          scope.date = date;
          scope.$apply( formatDateView(scope.date) );

          if (angular.isFunction(onSelect)) {
              onSelect();
          }
      };

      options.onOpen = function(date){
        picker.setDate(scope.date, false);
        picker.setMaxDate(moment(scope.max).toDate());
        picker.setMinDate(moment(scope.min).toDate());

        if (angular.isFunction(onOpen)){
          onOpen();
        }
      };

      var picker = new Pikaday(options);

      scope.$on('$destroy', function() {
          picker.destroy();
      });

      ngModelController.$parsers.push(function(data) {
        //convert data from view format to model format
        if(data){
          return formatDateModel(data); //converted  
        }
        
      });   
      ngModelController.$formatters.push(function(data) {
        //convert data from model format to view format
        if( data ){
          return formatDateView(data); //converted
        }
      });
    }
  };
});

