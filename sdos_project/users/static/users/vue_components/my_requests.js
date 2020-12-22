const Requests = {
	delimiters: ["[[", "]]"],
	template: `
		<ul class="list-group">
			<li class="list-group-item" v-for="(request, index) in requests" v-bind:key="request.id">
				<a style="float: left;" href="#">
					[[ request.username ]]
				</a>

				<div align='right'>
					<button class="btn btn-sm btn-primary" data-toggle="modal" :data-target="'#requestModal' + index" data-whatever="@mdo">
					View Request
					</button>
				</div>

				<div class="modal fade" :id="'requestModal' + index" tabindex="-1" role="dialog" :aria-labelledby="'requestModalLabel' + index" aria-hidden="true">
					<div class="modal-dialog" role="document">
						<div class="modal-content">

							<div class="modal-header">
								<h5 class="modal-title" :id="'requestModalLabel' + index">Request Details</h5>
								<button type="button" class="close" data-dismiss="modal" aria-label="Close">
									<span aria-hidden="true">&times;</span>
								</button>
							</div>

							<div class="modal-body">
								<table class="table">
									<tr>
										<th>Purpose:</th>
										<td>[[request.sop]]</td>
									</tr>
									<tr>
										<th>Mentee Expectations:</th>
										<td>[[request.expectations]]</td>
									</tr>
									<tr>
										<th>Mentee Commitment:</th>
										<td>[[request.commitment]]</td>
									</tr>
								</table>
							</div>
							
							<div class="modal-footer">
								<button v-on:click="accept_request(request.username, index)" class="btn btn-success"> Accept </button>
								<button v-on:click="reject_request(request.username, index)" class="btn btn-danger"> Reject </button>
								<button id="close-button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
							</div>
						</div>
					</div>
				</div>
			</li>
		</ul>
	`,
	data() {
		return {
			requests: []
		};
	},
	created() {
		let request_url = "http://127.0.0.1:8000/api/get_user_requests";

		axios.get(
			request_url
		)
		.then(response => {
			this.requests = response.data;
			console.log(this.requests);
		})
		.catch(error => {
			console.log("[ERROR]");
			console.log(error);
			this.requests = [];
		});
	},
	methods: {
		accept_request(username, index) {
			let request_url = "http://127.0.0.1:8000/api/accept_mentorship_request";

			axios.get(
				request_url,
				{
					'params': {
						'requestor': username
					}
				}
			)
			.then(response => {
				console.log("[SUCCESS]");
				this.requests = this.requests.filter(request => request.username !== username);
			})
			.catch(error => {
				console.log("[ERROR]");
				console.log(error);
			});

			$('#requestModal' + index).modal('hide');
			$('body').removeClass('modal-open');
			$('.modal-backdrop').remove();
		},
		reject_request(username, index) {
			let request_url = "http://127.0.0.1:8000/api/reject_mentorship_request";

			axios.get(
				request_url,
				{
					'params': {
						'requestor': username
					}
				}
			)
			.then(response => {
				console.log("[SUCCESS]");
				this.requests = this.requests.filter(request => request.username !== username);
			})
			.catch(error => {
				console.log("[ERROR]");
				console.log(error);
			});

			$('#requestModal' + index).modal('hide');
			$('body').removeClass('modal-open');
			$('.modal-backdrop').remove();
		}
	}
};