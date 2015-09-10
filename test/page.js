var ResultPage = function(){
  this.resultList = function() { return element.all(by.repeater('hit in hits')); };

  this.getFirstItemID = function(){
    return element.all(by.repeater('hit in hits')).then(function(hits) {
      var referenceNumber = hits[0].element(by.className('ng-binding'));
      a = referenceNumber.getText();
      return a;
    });
  };

  var dateRangeFrom = element(by.model('dateRange.from'));
  var dateRangeTo = element(by.model('dateRange.to'));

  log = function(e){
    e.getOuterHtml().then(function(value){
      console.log(value);
    });
  };

  this.filterOn = function(category, i, j){
    var block = element(by.id(category+'-agg'));
    var roundBtn = block.element(by.css('.cf-icon-plus-round'));
    roundBtn.isPresent().then(function(e){
      if(e) roundBtn.click();
    });

    var agg = block.all(by.css('.aggregation-value')).get(i-1);
    var numberAgg = agg.element(by.css('.number-agg')).getText().then(function(value){
      return Number(value);
    });

    if(!j){
      agg.element(by.tagName('input')).click();
      return numberAgg;
    }

    var expandBtn = agg.element(by.css('.cf-icon-down'));
    if(expandBtn){
      expandBtn.click();
      var subAgg = agg.all(by.css('.subaggregation-value')).get(j-1);
      var numberSubAgg = subAgg.element(by.css('.number-subagg')).getText().then(function(value){
        return Number(value);
      });
      subAgg.element(by.tagName('input')).click();
      return numberSubAgg;
    } else {
      agg.element(by.tagName('input')).click();
      return numberAgg;
    };
  };

  this.blockText = function(category){
    var block = element(by.id(category+'-agg'));
    return block.getText();
  };

  this.get = function(url){
    if (!url) {
      browser.get('')
    } else {
      browser.get(url);
    };
  };

  this.submitQuery = function(txt){
    element(by.model('queryText')).clear().sendKeys(txt);
    element(by.css('.search-submit-btn')).click();
  };

  this.clearFilter = function(){
    element(by.css('#clear-all-btn')).click();
  };

  function getValueFrom(selection, func){
    return element(selection).getText().then(function(value){
      if (func) {
        return func(value);
      } else {
        return value;
      }
    });
  }
  this.getResultInfo = function(){return element(by.css('.results_info-summary')).getText()};
  this.getTotalResults = function(){return getValueFrom(by.id('number_results'), parseInt)};
  this.getNumberSelected = function(){return getValueFrom(by.id('number_selected'), parseInt)};
  this.getDateRangeFrom = function(){return getValueFrom(by.model('dateRange.from'))};
  this.getTotalPage = function(){return getValueFrom(by.id('total_page'), parseInt)};
  this.getCurrentPage = function(){return getValueFrom(by.id('current_page'), parseInt)};

  this.paginateBy = function(n){
    var sizes = [10, 25, 50, 100];
    var i = sizes.indexOf(n);
    element.all(by.repeater('opt in sizeOptions')).get(i).click();
  };

  this.sortBy = function(n){
    //temporarily use 1-4 as parameter
    element.all(by.repeater('opt in sortOptions')).get(n).click();
  };

  this.filterByDate = function(from, to){
    // use format of "mm/dd/yyyy"
    element(by.model('dateRange.from')).clear().sendKeys(from);
    element(by.model('dateRange.from')).sendKeys(protractor.Key.TAB);
    element(by.model('dateRange.to')).clear().sendKeys(to);
    element(by.model('dateRange.to')).sendKeys(protractor.Key.TAB);
  };

  this.expandAllFilters = function(){
    element.all(by.css('.cf-icon-plus-round')).each(function(e){
      e.click();
    });
  };

  //pagination stuff
  this.getNextPage = function(){
    element(by.css('.pagination_next')).click();
  };
  this.getPrevPage = function(){
    element(by.css('.pagination_prev')).click();
  };

  //select items
  this.selectItems = function(ary){
    items = element.all(by.css('.search_result-selector'));
    ary.map(function(i){
      items.get(i).click();
    });
  };

  this.clearSelected = function(){
    element(by.id('clear-selected-btn')).click();
  };

};

module.exports = ResultPage;
