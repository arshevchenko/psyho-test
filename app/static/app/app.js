var psycho = angular.module("psycho", ["ngRoute"]);

psycho.config(function($routeProvider){
  $routeProvider
  .when('/',{
    templateUrl : 'static/view/main.html',
    controller : 'mainCtrl',
    controllerAs: 'main'
  })
  .when('/admin',{
    templateUrl: 'static/view/admin.html',
    controller: 'admAddTest',
    controllerAs: 'admin'
  });
});

psycho.controller('mainCtrl', mainCtrl);
psycho.controller('admAddTest', admAddTest);

function mainCtrl($http, $route, $scope){
  $scope.page_title = "Главная";
  $http.get('/api/test')
       .success(function(data){
         $scope.json_data = data;
       });

  $scope.remove_test = function(id){
    $http.delete('/api/admin/' + id).success(function(data){
        console.log("Removed");
    });
  }
}

function admAddTest($http, $route, $scope){
  $scope.send_new_test = function(form){
    $http.post('/api/admin', form)
         .success(function(data){
           console.log(data);
         });
  }
}
