var ResultPage = require('./page');

describe('search should present an input button and form', function() {
  beforeEach(function() {
    page = new ResultPage();
    page.clearFilter();
    page.submitQuery('mortgage');
    expect(page.getTotalResults()).toEqual(1967);
  });

  it('should search and present results', function() {
    var resultList = element.all(by.repeater('hit in hits'));
    expect(resultList.count()).toEqual(10);
    expect(resultList.get(2).getText()).toContain('mortgage');
  });

  it('apply date filter on results', function() {

    page.filterByDate('06/03/2015', '06/06/2015');
    expect(page.getTotalResults()).toEqual(13);
  });

  it('Increase result size', function() {
    page.paginateBy(10);
    expect(page.resultList().count()).toEqual(10);
    page.paginateBy(25);
    expect(page.resultList().count()).toEqual(25);
    page.paginateBy(50);
    expect(page.resultList().count()).toEqual(50);
    page.paginateBy(100);
    expect(page.resultList().count()).toEqual(100);
  });

  it('change sort option', function() {
    expect(page.getFirstItemID()).toEqual('1339697');
    page.sortBy(1);
    expect(page.getFirstItemID()).toEqual('1418697');
    page.sortBy(2);
    expect(page.getFirstItemID()).toEqual('1386568');
    page.sortBy(3);
    expect(page.getFirstItemID()).toEqual('1384221');
  });

});

describe('pagination should refresh or not refresh in different places;\n', function() {

  beforeEach(function() {
    page = new ResultPage();
    page.clearFilter();
    page.submitQuery('mortgage');
    expect(page.getTotalResults()).toEqual(1967);

    page.getNextPage();
    expect(page.getCurrentPage()).toEqual(2);
  });

  it('click next/prev page', function(){
    page.getNextPage();
    expect(page.getCurrentPage()).toEqual(3);
    page.getPrevPage();
    expect(page.getCurrentPage()).toEqual(2);
  });

  it('change date range filter refresh pagination', function(){
    page.filterByDate('04/18/2015', '06/17/2015');
    expect(page.getCurrentPage()).toEqual(1);
  });

  it('click a filter refresh pagination', function(){
    var elem = $('input[value="Mortgage-selected"]');
    elem.click();
    expect(page.getCurrentPage()).toEqual(1);
  });

  it('change page size refresh pagination', function(){
    page.paginateBy(25);
    expect(page.getCurrentPage()).toEqual(1);
  });

  it('change ranking method refresh pagination', function(){
    page.sortBy(2);
    expect(page.getCurrentPage()).toEqual(1);
  });

  it('new search refresh pagination', function(){
    page.submitQuery('bank');
    expect(page.getCurrentPage()).toEqual(1);
  });
});

describe('more like this\n', function() {
  beforeEach(function(){
    page = new ResultPage();
    page.clearFilter();
    page.submitQuery('mortgage');
    var total = page.getTotalResults();
    expect(total).toBeGreaterThan(0);
  });

  it('click more like this link should give results', function () {
    var elem = $(".search_result-mlt");
    elem.click();
    expect(page.getResultInfo()).toContain("results similar to complaint 1339697");
    expect(page.getFirstItemID()).toEqual('1329803');
  });
});

describe('filters: ', function(){
  beforeEach(function(){
    page = new ResultPage();
    page.get();
    page.submitQuery('bank');
    var total = page.getTotalResults();
    expect(total).toBeGreaterThan(0);
  });

  it('filter on two items under the same category should return results equal to sum of the two', function(){
    num1 = page.filterOn('Product', 1);
    num2 = page.filterOn('Product', 3);
    total = page.getTotalResults();

    num1.then(function(v1){
      num2.then(function(v2){
        expect(total).toEqual(v1+v2);
      });
    });
  });

  it('filter on two items under different category should return results equal to the 2nd one', function(){
    total = page.getTotalResults();
    num1 = page.filterOn('Product', 1);
    num2 = page.filterOn('Issue', 2);
    total = page.getTotalResults();
    expect(total).toEqual(num2);
  });

  it('filter on parent, then on child, total should equal to child ', function(){
    total = page.getTotalResults();
    num = page.filterOn('Product', 2, 2);
    total = page.getTotalResults();
    expect(total).toEqual(num);
  });

  it('the last filter should not change the agg result of the category', function() {
    txt1 = page.blockText('Product');
    page.filterOn('Product', 1);
    txt2 = page.blockText('Product');
    txt1.then(function (v1) {
      txt2.then(function (v2) {
        expect(v1).toEqual(v2);
      });
    });
  });

  it('check one item and one or more of its children, then check another item on the same level, ' +
    'should return results equal to the sum of its children and the other item', function(){
    num1 = page.filterOn('Product', 1, 1);
    num2 = page.filterOn('Product', 2);
    total = page.getTotalResults();
    num1.then(function(v1){
      num2.then(function(v2){
        expect(total).toEqual(v1+v2);
      });
    });
  });

  it('filter on two parent, each with child, total should equal to two children', function(){
    num1 = page.filterOn('Product', 1, 1);
    num2 = page.filterOn('Product', 2, 1);
    total = page.getTotalResults();
    num1.then(function(v1){
      num2.then(function(v2){
        expect(total).toEqual(v1+v2);
      });
    });
  });

  it('filter on two parent, each with child, from the same category; then filter on another item from' +
    'other category. total should equal to the latest filter applied.', function(){
    num1 = page.filterOn('Product', 1, 1);
    num2 = page.filterOn('Product', 2, 1);
    num3 = page.filterOn('State', 1);
    total = page.getTotalResults();
    expect(num3).toEqual(total);
  });

  it('filter on, then filter off, total should revert', function(){
    num1 = page.filterOn('Product', 1, 1);
    num2 = page.filterOn('Product', 2, 1);
    page.filterOn('State', 1);
    num3 = page.filterOn('State', 1);
    total = page.getTotalResults();
    num1.then(function(v1){
      num2.then(function(v2){
        expect(total).toEqual(v1+v2);
      });
    });
  });

  it('filter on, then search, filter not reset', function(){
    page.filterOn('Product', 1);
    page.submitQuery('credit');
    total = page.getTotalResults();
    expect(total).toEqual(435);
  });

});

describe('Aggregations should be ordered properly;\n', function() {
  beforeEach(function(){
    page = new ResultPage();
    page.clearFilter();
    page.submitQuery('Mortgage');
    var total = page.getTotalResults();
    expect(total).toBeGreaterThan(0);
  });

  it('should display aggregations in order', function () {

    var firstAgg = element(by.repeater('agg in aggregationArray').
    row(0).column('agg.name'));
    var secondAgg = element(by.repeater('agg in aggregationArray').
    row(1).column('agg.name'));
    var thirdAgg = element(by.repeater('agg in aggregationArray').
    row(2).column('agg.name'));

    expect(firstAgg.getText()).toContain('MATCHED COMPANY');
    expect(secondAgg.getText()).toContain('PRODUCT');
    expect(thirdAgg.getText()).toContain('ISSUE');
  });
});

describe('more like this search', function(){
  it('should return results', function(){
    page = new ResultPage();
    page.get('/#/mlt?id=1324595&field=what_happened');
    expect(page.getTotalResults()).toEqual(6771);
  });

  it('should return results', function(){
    page = new ResultPage();
    page.get('/#/mlt?id=1324595');
    expect(page.getTotalResults()).toEqual(7470);
  });
});

describe('select items to export', function(){
  beforeEach(function(){
    page = new ResultPage();
    page.clearFilter();
    page.submitQuery('Mortgage');
    var total = page.getTotalResults();
    expect(total).toBeGreaterThan(0);
  });

  iit('select items should persist across searches, unless explicitly cleared', function(){
    page.selectItems([1,3]);
    expect(page.getNumberSelected()).toEqual(2);
    page.submitQuery('bank');

    page.selectItems([2]);
    expect(page.getNumberSelected()).toEqual(3);

    page.clearSelected();
    page.selectItems([0]);
    expect(page.getNumberSelected()).toEqual(1);

  });

});
