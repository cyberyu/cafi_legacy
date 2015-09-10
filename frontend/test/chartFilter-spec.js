describe('directive: chartFilter in D3', function() {
  var $compile,
      $rootScope;

  // Load the myApp module, which contains the directive
  beforeEach(module('SearchApp'));

  // Store references to $rootScope and $compile
  // so they are available to all tests in this describe block
  beforeEach(inject(function(_$compile_, _$rootScope_){
    // The injector unwraps the underscores (_) from around the parameter names when matching
    compile = _$compile_;
    rootScope = _$rootScope_;
  }));

  it('Replaces the element with the appropriate content', function() {
    // Compile a piece of HTML containing the directive
    var element = compile('<chart-filter></chart-filter>')(rootScope);

    // Check that the compiled element contains the templated content
    expect(element.html()).toContain('<div id="date_chart">');
  });

});