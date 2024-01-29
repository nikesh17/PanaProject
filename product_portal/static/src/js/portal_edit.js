const edit_negotiation_request = (negotiationId) => {
            console.log("heloo");
            console.log(negotiationId)
           var modal = new Modal(document.getElementById('new_modal'));
           modal.show();
           document.getElementById('save_changes').addEventListener('click',e=>{

            save_changes(negotiationId);
           });
        };
        const close_modal = () => {
                $('#new_modal').modal('hide');
        }
//        Following save_changes is the function to update the values in db
        const save_changes = (negotiationId) =>{
        console.log(negotiationId)
        const updated_expected_price = document.getElementById('expected_price').value;
        const updated_customer_status = document.getElementById('customer_status').value;
//        const updated_quantity = document.getElementById('quantity').value;
//         console.log(updated_expected_price);
         fetch('/update_negotiation_record', {
                   method: 'POST',
                  headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                'negotiation_id':negotiationId,
                 'updated_expected_price': updated_expected_price,
                 'updated_customer_status': updated_customer_status,
//                 'updated_quantity': updated_quantity
                })
              })
              .then(function (response) {
                if (response.ok) {
                  return response.json();
                  setTimeout(() => {
                    window.location.reload()
                  }, 800)
                }
                throw new Error('Network response was not ok.');
              })
              .then(function (data) {
              window.location.reload()
                // Process the retrieved data
                // Populate the edit form fields or perform other actions with the data
              })
              .catch(function (error) {
                console.error('There was a problem with the fetch operation:', error);
                // Handle errors or exceptions here
              });
                }

//This function is for deleting record of price negotiation
const delete_record = (negotiationId) => {
  fetch(`/delete/negotiation-request/${negotiationId}`, {
    method: 'DELETE'
  })
    .then(function(response) {
      if (response.ok) {
        console.log("Record deleted Successfully!!");
        setTimeout(()=>{
          window.location.reload();
        },800)
      } else {
        console.log("Delete operation Failed");
      }
    })
    .catch(function(error) {
      console.error('There was a problem with the delete operation:', error);
      // Handle errors or exceptions here
    });

  console.log("Initiating deletion for record ID:", negotiationId);
};
    //function editNegotiation(negotiationId=123) {
    //  console.log(negotiationId);
    //  console.log("Hello from js");
    //
    //  fetch('/retrieve_negotiation_data', {
    //    method: 'POST',
    //    headers: {
    //      'Content-Type': 'application/json'
    //    },
    //    body: JSON.stringify({ 'negotiation_id': negotiationId })
    //  })
    //  .then(function (response) {
    //    if (response.ok) {
    //      return response.json(); // assuming the response is JSON
    //    }
    //    throw new Error('Network response was not ok.');
    //  })
    //  .then(function (data) {
    //    // Process the retrieved data
    //    // Populate the edit form fields or perform other actions with the data
    //  })
    //  .catch(function (error) {
    //    console.error('There was a problem with the fetch operation:', error);
    //    // Handle errors or exceptions here
    //  });
    //}