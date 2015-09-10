
describe('save Search service', function () {
  var saveSearchService, httpBackend;

  beforeEach(module('SearchApp'));

  beforeEach(inject(function (_saveSearchService_, $httpBackend) {
    saveSearchService = _saveSearchService_;
    httpBackend = $httpBackend;
  }));

  it('should return a success value on ping', function () {
    httpBackend.whenPOST('/_search/save').respond(200, 'Saved Successfully');
    saveSearchService.save().then(function( response ) {
      expect( response.data ).toEqual('Saved Successfully');
    });
    httpBackend.flush();
  });

});
