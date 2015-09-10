describe('page modals and modal scopes', function(){
   // load the controller's module
  beforeEach(module('SearchApp'));

  var fakeModal = {
      result: {
          then: function(confirmCallback, cancelCallback) {
              //Store the callbacks for later when the user clicks on the OK or Cancel button of the dialog
              this.confirmCallBack = confirmCallback;
              this.cancelCallback = cancelCallback;
          }
      },
      close: function( item ) {
          //The user clicked OK on the modal dialog, call the stored confirm callback with the selected item
          this.result.confirmCallBack( item );
      },
      dismiss: function( type ) {
          //The user clicked cancel on the modal dialog, call the stored cancel callback
          this.result.cancelCallback( type );
      }
  };
  beforeEach( inject(function($modal) {
    spyOn($modal, 'open').and.returnValue(fakeModal);
  }));

  beforeEach(inject(['$controller', '$rootScope', '$modal', function( $controller, $rootScope, _$modal_) {
    scope = $rootScope.$new();
    controller = $controller;
    rootScope = $rootScope;
    modal = _$modal_;

    controller('searchController', {
      $scope: scope,
      $modal: modal
    });

  }]));

  it('Opens an export modal and returns values on success', function () {
    spyOn(scope, 'exportHref').and.returnValue('true');
    expect( scope.modal.modalInstanceExport).toBeUndefined();
    scope.exportItemSelector = 'All Records';
    scope.modal.openExportModal('random');
    expect( scope.modal.modalInstanceExport).toBeDefined();
    scope.modal.modalInstanceExport.close('500 records');
    expect( scope.exportItemSelector ).toEqual('500 records');
    expect( scope.exportHref ).toHaveBeenCalled();
  });

  it('Export modal esponds properly to cancellations', function(){
    spyOn(scope, 'exportHref').and.returnValue('true');
    expect( scope.modal.modalInstanceExport).toBeUndefined();
    scope.modal.openExportModal('hi there');
    expect( scope.modal.modalInstanceExport.dismiss).toBeDefined();
    scope.modal.modalInstanceExport.dismiss('cancelled');
    expect( scope.modal.modalInstanceExport.dismissed ).toBeTruthy();
  });

  it('Opens a save modal and returns values on success', function () {
    expect( scope.modal.modalInstanceSave).toBeUndefined();
    scope.modal.openSaveModal('random');
    expect( scope.modal.modalInstanceSave).toBeDefined();
    scope.mycallbackval = false;
    function mycallback(){
      scope.mycallbackval = true;
    }
    scope.modal.modalInstanceSave.close( mycallback );
    expect( scope.mycallbackval ).toBeTruthy();
  });

  it('Save modal esponds properly to cancellations', function(){
    expect( scope.modal.modalInstanceSave).toBeUndefined();
    scope.modal.openSaveModal('hi there');
    expect( scope.modal.modalInstanceSave.dismiss).toBeDefined();
    scope.modal.modalInstanceSave.dismiss('cancelled');
    expect( scope.modal.modalInstanceSave.dismissed ).toBeTruthy();
  });

});
