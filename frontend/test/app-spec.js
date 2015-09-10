describe('App test suite', function() {

  var controller, scope, httpBackend, client, location;

  beforeEach(module('SearchApp', function( $provide ) {

      client = jasmine.createSpyObj("client", ['search', 'cluster']);

      client.search.and.returnValue(
        {
          then: function( body ) {

          }
        }
      );
      client.cluster = {
        state: function( obj ) {
          return {
            then: function( cb ) {
              cb({});
              return {
                catch: function( cb ) {
                  cb({})
                }
              }
            }
          }
        }
      };

      $provide.value("client", client);
    })
  );

  beforeEach(inject(['$controller', '$rootScope', '$location', '$modal', 'client', function( $controller, $rootScope, $location, $modal, _client_ ) {
    scope = $rootScope.$new();
    controller = $controller;
    client = _client_;
    location = $location;
    rootScope = $rootScope;
    modal = $modal;

    controller('searchController', {
      $scope: scope,
      client: client
    });

    // Modal Spies:
    var fakeModal = {
      result: {
          then: function (confirmCallback, cancelCallback) {
              this.confirmCallBack = confirmCallback;
              this.cancelCallback = cancelCallback;
              return this;
          },
          catch: function (cancelCallback) {
              this.cancelCallback = cancelCallback;
              return this;
          },
          finally: function (finallyCallback) {
              this.finallyCallback = finallyCallback;
              return this;
          }
      },
      close: function (item) {
          this.result.confirmCallBack(item);
      },
      dismiss: function (item) {
          this.result.cancelCallback(item);
      },
      finally: function () {
          this.result.finallyCallback();
      }
    };
    spyOn(modal, 'open').and.returnValue(fakeModal);

  }]));

  it('it should invoke client.search', function() {
    scope.queryText = "merc";
    scope.sendQuery();
    expect(client.search).toHaveBeenCalled();
  });
  
  it('getComplaints should return number of all true references selected', function() {
    scope.selectedComplaints = {
      '1234567': true,
      '1435672': false
    };
    expect( scope.getComplaintsSelected() ).toBe(1);
  });

  it('queryBuilder queryFromValue yields an integer page number', function() {
    scope.pager.page = 2;
    scope.size = 2;
    expect( scope.queryBuilder.query.getQueryFromValue() ).toBe(2);
  });

  it('queryBuilder appendQueryText appends new search term', function() {
    scope.queryText = "Mortgage";
    scope.queryBuilder.query.appendQueryText("Loan");
    expect( scope.queryText).toBe("Mortgage Loan");
  });

  it('if queryText is blank, default to *', function(){
    scope.queryType = 'norm';
    var query = scope.queryBuilder.query.makeSearchQuery().toJSON();
    expect(scope.queryText).toBe('*');  //queryText get changed
    expect(query).toContainKeys(['query_string']);  //query body get built
  });

  it('queryBuilder appendQueryText replaces null query text with new text', function() {
    scope.queryText = null;
    scope.queryBuilder.query.appendQueryText("Loan");
    expect( scope.queryText).toBe("Loan");
  });

  it('q query properly detects More Like This', function() {
    scope.queryType = 'mlt';
    scope.mlt_id = 1234;
    scope.queryText = 'hello';
    var query = scope.queryBuilder.query.detectMoreLikeThis().toJSON();
    expect( query ).toContainKeys(['mlt']);
  });

  it('q query properly detects normal type', function(){
    scope.queryType = 'norm';
    scope.queryText = 'hello';
    var query = scope.queryBuilder.query.detectMoreLikeThis().toJSON();
    expect( query ).toContainKeys(['match']);

    scope.queryText = 'hello AND world';
    var query = scope.queryBuilder.query.detectMoreLikeThis().toJSON();
    expect( query ).toContainKeys(['query_string']);
  });

  it('postFilter returns an AND filter when filter exists', function(){
    scope.filters = {
      terms: {'Company': {'Company Name': true }},
      range: null,
      categories: ['Company'],
    };
    scope.aggregations = {
      'Company': { 'name': 'Company',
        'field': 'name',
        'size': 8,
        'subagg': null
      }
    };
    var query = scope.queryBuilder.filter.makePostFilter().toJSON();
    expect( query ).toContainKeys(['and']);
    expect( query.and.filters[0] ).toContainKeys(['bool']);
    expect( query.and.filters[0].bool ).toContainKeys(['should']);
  });
  it('postFilter returns only a range AND when no checkboxes applied', function(){
    scope.filters = {
      terms: null,
      range: null,
      categories: [],
    };
    scope.aggregations = {
      'Company': { 'name': 'Company',
        'field': 'name',
        'size': 8,
        'subagg': null
      }
    };
    var postfilter = scope.queryBuilder.filter.makePostFilter().toJSON();
    expect( postfilter.and.filters[0] ).toContainKeys(['range']);
  });

  // Show-Hide Tracker
  it('Show-Hide helpers act properly given shown', function(){
    scope.showHideTracker.shown = {
      'Product': true,
      'Issue': true,
      'Company': true,
      'dateRange': true
    };
    scope.showHideTracker.onToggleClick('Product');
    expect( scope.showHideTracker.shown['Product']).toBe(false);

    scope.showHideTracker.onToggleClick('Rando Category');
    expect( scope.showHideTracker.shown['Rando Category']).toBe(true);

    expect( scope.showHideTracker.getToggleClass('Product') ).toBe('cf-icon-down');
    scope.showHideTracker.shown.Product = true;
    expect( scope.showHideTracker.getToggleClass('Product') ).toBe('cf-icon-up');

    expect( scope.showHideTracker.getParentToggleClass('Product') ).toBe('cf-icon-minus-round');
    scope.showHideTracker.shown.Product = false;
    expect( scope.showHideTracker.getParentToggleClass('Product') ).toBe('cf-icon-plus-round');

    expect( scope.showHideTracker.checkIfShown('Product') ).toBe(false);
    scope.showHideTracker.shown.Product = true;
    expect( scope.showHideTracker.checkIfShown('Product') ).toBe(true);

  });
  // Test no longer required as we removed the first page.
  // it('SearchPerformed should set results to true and change search class', function(){
  //   scope.resultsShown = false;
  //   scope.search_creator_class = 'search_creator';

  //   scope.searchPerformed();
  //   expect( scope.resultsShown ).toBe( true );
  //   expect( scope.search_creator_class ).toBe( 'search_creator-small');
  // });

  it('Pager functions should increment, decrement and assign classes properly', function(){
    scope.size = 10;
    scope.pager.page = 1;
    scope.pager.totalPages = 1;
    scope.pager.next();
    expect( scope.pager.page ).toBe(1);
    scope.pager.totalPages = 10;
    scope.pager.next();
    expect( scope.pager.page ).toBe(2);
    scope.pager.prev();
    expect( scope.pager.page ).toBe(1);

    expect( scope.pager.prevClass() ).toBe('btn pagination_prev btn__disabled');
    expect( scope.pager.nextClass() ).toBe('btn pagination_next');

  });

  it('checkifExportSelected should yield false if All selected', function(){
    scope.exportItemSelector = 'All Returned';
    expect( scope.checkIfExportSelected() ).toBeFalsy();
  });

  it('checkifExportSelected should yield true if anything other than "all" selected', function(){
    scope.exportItemSelector = '2 Selected Records';
    expect( scope.checkIfExportSelected() ).toBeTruthy();
  });

  it('genExportBody should generate an ID query when user asks for selected records', function(){
    scope.selectedComplaints = [];
    expect( scope.genExportBody() ).toContainKeys(['query']);
    scope.selectedComplaints = ['12345', '123456'];
    scope.exportItemSelector = 'Only Selected Complaints (2)';
    expect( scope.genExportBody().query ).toContainKeys(['ids']);
  });

  it('genExportBody should use filtered query when filter(s) is on', function() {
    scope.filters.terms = {"Product":{"Debt collection":{"value":true}}};
    scope.queryText = '"credit card" AND "credit reporting" AND citibank'
    body = scope.genExportBody();
    expect(body.query).toContainKeys(['filtered']);
    expect(body.query.filtered).toContainKeys(['query', 'filter']);
  });

  it('genExportHref should include the correct url params for export URL', function() {
    scope.exportFormat = 'CSV'
    expect( scope.genExportHref() ).toContain('CSV');
    expect( scope.genExportHref() ).toContain('&search=');
  });

  it('export item selector yields the correct array of options based on selections', function(){
    scope.selectedComplaints = [];
    scope.number_results = 5;
    expect( scope.exportItemSelectorOptions() ).not.toContain('Only Selected Complaints (2)');
    expect( scope.exportItemSelectorOptions() ).toContain('All Returned Complaints (5)');
    
    scope.selectedComplaints = ['12345', '123456'];
    expect( scope.exportItemSelectorOptions() ).toContain('Only Selected Complaints (2)');
  });

  it('setNewScopeFromQuery sets variables based on query returns', function(){
    var body = {
      hits: {
        hits: {
          hit: 'whoah'
        },
        total: 1234
      },
      aggregations: { cr_date: { cr_date: { buckets: ['05/12/2015', '08/12/2015'] }}},
      took: 12
    };
    scope.pager = {};
    scope.searchPerformed = function(){ return true };
    scope.pager.page = 1;
    scope.queryText = 'hi';
    scope.time_returned = new Date();
    scope.hits = body.hits.hits;
    scope.lastQueryText = scope.queryText;
    scope.aggregationResults = body.aggregations;
    scope.chartData = body.aggregations.cr_date.cr_date.buckets;
    scope.number_results = body.hits.total;
    scope.time_taken = body.took;
    scope.searchPerformed();
    scope.err = true;

    scope.setNewScopeFromQuery( body );

    expect( scope.err ).toBe( false );
  });

  it('if options.reset is false, not reset scope', function(){
    scope.size = 25;
    scope.setSendQueryOptions();
    expect(scope.size).toEqual(25);
  });

  it('aggregations object should convert to an array', function(){
    scope.aggregations = {
      'Company': { 'name': 'Company',
        'field': 'name',
        'size': 8,
        'order': 1,
        'subagg': null
      },
      'Issue': { 'name': 'Issue',
        'field': 'category_level_1.raw',
        'size': 100,
        'order': 2,
        'subagg': {
            'name': 'category.raw',
            'field': 'category.raw',
            'size': 100
        }
      }
    };

    var newArray = scope.aggregationArray;
    expect( newArray ).toEqual(jasmine.any(Array));
    expect( newArray[0] ).toContainKeys(['name', 'order']);
    expect( newArray[1] ).toContainKeys(['name', 'order']);
  });

  it('various strings should/not use synonym search', function(){
    func = scope.queryBuilder.query.shouldUseSynonym;

    scope.queryText = 'Credit card';
    expect(func()).toBe(true);
    scope.queryText = 'wi_fi';
    expect(func()).toBe(true);
    scope.queryText = '+credit';
    expect(func()).toBe(false);
    scope.queryText = 'credit AND card';
    expect(func()).toBe(false);
    scope.queryText = 'credit OR card';
    expect(func()).toBe(false);
    scope.queryText = 'credit TO card';
    expect(func()).toBe(false);
    scope.queryText = "credit NOT card";
    expect(func()).toBe(false);
  });


  it('show Hide Tracker should return correct class on toggle', function() {
    scope.searchTips.tipStatus = false;
    expect( scope.searchTips.returnTipStatus() ).toBe(false);
    scope.searchTips.tipStatus = true;
    expect( scope.searchTips.returnTipStatus() ).toBe(true);
    expect( scope.searchTips.checkTipClass() ).toBe('cf-icon cf-icon-up');
    scope.searchTips.tipStatus = false;
    expect( scope.searchTips.checkTipClass() ).toBe('cf-icon cf-icon-down');
    scope.searchTips.toggleTip();
    expect( scope.searchTips.tipStatus ).toBe(true);
  });

  it('suggest should get data',
    inject(function($httpBackend) {
      scope.queryText = 'w';

      $httpBackend.when('POST', '/_suggest').respond(200, '["word1", "word2"]');
      scope.suggest(scope.queryText).then(function(v){
        expect(v).toEqual(['word1', 'word2']);
      });
      $httpBackend.flush();
    })
  );
  
  it('save handler should adjust search status and name', function(){
    scope.savedSearch.status = 'random status';
    scope.queryText = 'My mock query text';
    scope.savedSearch.saveHandler();
    expect(scope.savedSearch.status).toBe('Search saved.');
    expect(scope.savedSearch.savedSearchName ).toContain('My mock query text');
  });

  it('should generate correct save parameters', function() {
    scope.savedSearch.status = false;
    expect(scope.savedSearch.getStatusClass() ).toBe('cf-icon-save');
    scope.savedSearch.status = 'Saved Successfully';
    expect( scope.savedSearch.getStatusClass() ).toBe('cf-icon-approved-round');
  });

  it('setScopeParamsFromPath should correctly parse the url and extract params', function(){
    location.url('/q?filters=Product:Debt%20collection:product.raw:Other%20(phone,%20health%20club,%20etc.)&filters=Product:Debt%20collection:product.raw:Credit%20card&filters=Product:Debt%20collection:product.raw:Medical&filters=Product:Debt%20collection:product.raw:Payday%20loan&filters=Product:Mortgage&txt=debt%20mortgage&date_from=2015-03-18&date_to=2015-06-18&size=25&sort=created_time&page=2');
    //filters = {"Product":{"Debt collection":{"value":true,"product.raw":{"Other (phone, health club, etc.)":true,"Credit card":true,"Medical":true,"Payday loan":true}},"Mortgage":{"value":true}}};
    filters = {"Product": {
      "Debt collection":
      {"value":true,
        "product.raw":{
          "Other (phone, health club, etc.)": {"value": true},
          "Credit card": {"value": true},
          "Medical":{"value": true},
          "Payday loan":{"value": true}}
      },
      "Mortgage":{"value":true}}};
    scope.setScopeParamsFromPath(location);

    expect(scope.size).toEqual(25);
    expect(scope.queryText).toEqual('debt mortgage');
    expect(scope.sort).toEqual('created_time');
    expect(JSON.stringify(scope.filters.terms)).toEqual(JSON.stringify(filters));
    expect(scope.dateRange.from).toEqual("2015-03-18");
    expect(scope.dateRange.to).toEqual("2015-06-18");
  });

  it('scope.hashParams.filters should be built correct from scope.filters.terms', function(){
    scope.filters.terms = {"Product": {
                              "Debt collection":
                              {"value":true,
                                "product.raw":{
                                  "Other (phone, health club, etc.)": {"value": true},
                                  "Credit card": {"value": true},
                                  "Medical":{"value": true},
                                  "Payday loan":{"value": true}}
                              },
                              "Mortgage":{"value":true}}};
    scope.buildFilterStrings(scope.filters.terms, null);
    filters = ["Product:Debt collection", "Product:Debt collection:product.raw:Other (phone, health club, etc.)","Product:Debt collection:product.raw:Credit card","Product:Debt collection:product.raw:Medical","Product:Debt collection:product.raw:Payday loan","Product:Mortgage"];

    expect(JSON.stringify(scope.hashParams.filters)).toEqual(JSON.stringify(filters));

  });

  it('changeLocation should create good url from scope params', function(){
    scope.size = 25;
    scope.page = 3;
    scope.queryText = "credit";
    scope.queryType = 'norm';
    //scope.filters.terms = {"Product":{"Debt collection":{"value":true,"product.raw":{"Other (phone, health club, etc.)":true,"Credit card":true,"Medical":true,"Payday loan":true}},"Mortgage":{"value":true}}};
    scope.filters.terms = {"Product": {
      "Debt collection":
      {"value":true,
        "product.raw":{
          "Other (phone, health club, etc.)": {"value": true},
          "Credit card": {"value": true},
          "Medical":{"value": false},
          "Payday loan":{"value": true}}
      },
      "Mortgage":{"value":true}}};
    scope.dateRange.from = '2015-03-18';
    scope.dateRange.to = '2015-06-18';
    scope.pager.page = 3;
    scope.queryBuilder.makeRequestBody();
    scope.sort = 'created_time';
    scope.changeLocation();
    url = '/q?filters=Product:Debt%20collection&filters=Product:Debt%20collection:product.raw:Other%20(phone,%20health%20club,%20etc.)&filters=Product:Debt%20collection:product.raw:Credit%20card&filters=Product:Debt%20collection:product.raw:Payday%20loan&filters=Product:Mortgage&txt=credit&fields=Narratives&date_from=2015-03-18&date_to=2015-06-18&size=25&sort=created_time&page=3';

    expect(url).toEqual(location.url());
  });

  it('makePostFilter should build right query body', function(){
    scope.filters.terms = {"Product":{"Debt collection":{"product.raw":{"Credit card":{"value":false},"Medical":{"value":true},"Other (phone, health club, etc.)":{"value":true},"Payday loan":{"value":true}},"value":true},"Mortgage":{"value":true}}}
    scope.dateRange.from = "2015-03-18";
    scope.dateRange.to = "2015-08-26";
    result = {"and":{"filters":[{"bool":{"should":[{"and":{"filters":[{"term":{"product_level_1.raw":"Debt collection"}},{"terms":{"product.raw":["Medical","Other (phone, health club, etc.)","Payday loan"]}}]}},{"term":{"product_level_1.raw":"Mortgage"}}]}},{"range":{"created_time":{"from":"2015-03-18","to":"2015-08-26"}}}]}}
    andFilter = scope.queryBuilder.filter.makePostFilter();
    expect(JSON.stringify(andFilter)).toEqual(JSON.stringify(result));
  });

  it('if normal query, search should use relevant field(s)', function(){
    scope.queryType = 'norm';

    scope.searchFields = 'Narratives';

    scope.queryText = 'bank';
    q = scope.queryBuilder.query.detectMoreLikeThis();
    result = {"match":{"what_happened":{"query":"bank"}}};
    expect(JSON.stringify(q)).toEqual(JSON.stringify(result));

    scope.queryText = 'bank AND loan';
    q = scope.queryBuilder.query.detectMoreLikeThis();
    result = {"query_string":{"query":"bank AND loan","fields":["what_happened"]}};
    expect(JSON.stringify(q)).toEqual(JSON.stringify(result));

    scope.searchFields = 'All Data';

    scope.queryText = 'bank';
    q = scope.queryBuilder.query.detectMoreLikeThis();
    result = {"match":{"_all":{"query":"bank"}}};
    expect(JSON.stringify(q)).toEqual(JSON.stringify(result));

    scope.queryText = 'bank AND loan';
    q = scope.queryBuilder.query.detectMoreLikeThis();
    result = {"query_string":{"query":"bank AND loan","fields":["_all"]}};
    expect(JSON.stringify(q)).toEqual(JSON.stringify(result));
  });

  it('clearSelectedComplaints should clear all selected complaints', function(){
    scope.SelectedComplaints = {12345: true};
    scope.clearSelectedComplaints();
    expect(Object.keys(scope.selectedComplaints).length).toEqual(0);
  })
});





