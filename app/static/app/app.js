var psycho = angular.module("psycho", ["ngRoute"]);
var main_title = " - Тестирование";

psycho.config(function($routeProvider, $locationProvider){
  $routeProvider
  .when('/',{
    templateUrl : 'static/view/main.html',
    controller : 'mainCtrl',
    controllerAs: 'main'
  })
  .when('/admin',{
    templateUrl: 'static/view/admin.html',
    controller: 'admPanel',
    controllerAs: 'admin'
  })
  .when('/test',{
    templateUrl: 'static/view/test',
    controller: 'showTests',
    controllerAs: 'tests'
  });

  $locationProvider.html5Mode(true);
});

psycho.controller('mainCtrl', mainCtrl);
psycho.controller('admPanel', admPanel);
psycho.controller('showTests', showTests);

function mainCtrl($http, $route, $scope){
  $scope.page_title = "Главная" + main_title;

  $scope.send_user = function(form){
      $http.post('/api/login', form)
           .success(function(data){
             console.log(data["uid"]);
           });
  }
}

function admPanel($http, $route, $scope){
  $scope.page_title = "Панель администрирования" + main_title;
  
  $scope.send_new_test = function(form){
    $http.post('/api/admin', form)
         .success(function(data){
           console.log(data);
         });
  }
}
