/*
 * AngularJS front‑end application for the Fulfilment Insights Hub.
 *
 * This script defines a simple AngularJS module and controller that
 * loads summary metrics from the backend and allows users to submit
 * natural‑language questions to the chat endpoint.  The results are
 * displayed in a conversation‑style format.  You can expand this
 * script with additional components, services and charts as your
 * application grows.
 */

(() => {
  const app = angular.module('insightsApp', []);

  app.controller('MainController', ['$http', function($http) {
    const vm = this;

    // Holds the summary metrics returned from the API
    vm.summary = {};
    // Holds the current query entered by the user
    vm.query = '';
    // Conversation history; array of {query: string, answer: string}
    vm.responses = [];

    /**
     * Fetch insights summary from the backend API.
     */
    vm.loadSummary = function() {
      $http.get('/api/insights-summary/')
        .then(function(response) {
          vm.summary = response.data;
        })
        .catch(function(error) {
          console.error('Failed to load summary', error);
        });
    };

    /**
     * Send the user's query to the chat endpoint and append the result
     * to the conversation history.
     */
    vm.sendQuery = function() {
      if (!vm.query) {
        return;
      }
      const currentQuery = vm.query;
      // Clear the input field before the async call returns
      vm.query = '';
      $http.post('/api/chat/', { query: currentQuery })
        .then(function(response) {
          vm.responses.push({ query: currentQuery, answer: response.data.response });
        })
        .catch(function(error) {
          console.error('Chat request failed', error);
          const errMsg = error.data && error.data.error ? error.data.error : 'An error occurred';
          vm.responses.push({ query: currentQuery, answer: errMsg });
        });
    };

    /**
     * Convert snake_case keys into human‑readable titles.
     * Example: 'mtd_total_orders' becomes 'Mtd Total Orders'.
     *
     * @param {string} key The original metric key.
     * @returns {string} Title‑cased label
     */
    vm.formatKey = function(key) {
      return key
        .split('_')
        .map(part => part.charAt(0).toUpperCase() + part.slice(1))
        .join(' ');
    };

    // Load summary data on initialisation
    vm.loadSummary();
  }]);
})();
