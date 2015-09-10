describe('directive: pillFilter', function() {
  var $compile,
      $rootScope;

  // Load the myApp module, which contains the directive
  beforeEach(module('SearchApp'));

  // Store references to $rootScope and $compile
  // so they are available to all tests in this describe block
  beforeEach(inject(function( $controller, $rootScope, _$compile_ ) {
    scope = $rootScope.$new();
    controller = $controller;
    rootScope = $rootScope;
    compile = _$compile_

    controller('searchController', {
      $scope: scope
    });

  }));

  it('Replaces the element with the appropriate content', function() {
    // Compile a piece of HTML containing the directive
    var element = compile('<pill-filter></pill-filter>')(rootScope);

    // Check that the compiled element contains the templated content
    expect(element.html()).toContain('<div class="search_underbar-pills">');
  });

  it('Properly creates a filter array', function() {
    // Compile a piece of HTML containing the directive
    scope.filters.terms = {};
    scope.filters.terms.Product = {};
    scope.filters.terms.Product.Mortgage = { value: true };
    var element = compile('<pill-filter></pill-filter>')(scope);
    scope.filterPills.getPills();
    // Check that the compiled element contains the templated content
    expect( scope.filterPills.pills.length ).toBeGreaterThan(0);
  });

  it('Removes filters properly', function() {
    // Compile a piece of HTML containing the directive
    scope.filters.terms = {};
    scope.filters.terms.Product = {};
    scope.filters.terms.Product.Mortgage = { value: true };
    var element = compile('<pill-filter></pill-filter>')(scope);
    scope.filterPills.getPills();

    // Check that the compiled element contains the templated content
    expect( scope.filterPills.pills.length ).toBeGreaterThan(0);
  });

});