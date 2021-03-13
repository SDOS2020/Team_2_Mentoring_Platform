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
								<h5 class="modal-title" :id="'requestModalLabel' + index">
									Request Details
								</h5>
								<button type="button" class="close" data-dismiss="modal" aria-label="Close">
									<span aria-hidden="true">&times;</span>
								</button>
							</div>

							<div class="modal-body">
								<table class="table">
									<tr>
										<th>Name:</th>
										<td>[[ request.name ]]</td>
									</tr>
								</table>
								
								<table class="table">
									<th>Education:</th>
									<tr v-for="edu in request.educations">
										<td>
											<div style="float: right;">
												<i>
													[[ edu.start_date ]] <b>to</b>
													<br>
													[[ edu.end_date ]]
												</i>
											</div>
											
											<div style="width: 70%">
												<b> [[ edu.qualification ]] </b>
											</div>

											<br/>
											<b> [[ edu.organization ]] </b>
											<br/>
											[[ edu.detail ]]
											<hr>
										</td>
									</tr>
								</table>
								
								<table class="table">
									<tr>
										<th>Purpose:</th>
										<td>[[ request.sop ]]</td>
									</tr>
									<tr>
										<th>Mentee Expectations:</th>
										<td>[[ request.expectations ]]</td>
									</tr>
									<tr>
										<th>Mentee Commitment:</th>
										<td>[[ request.commitment ]]</td>
									</tr>
								</table>
							</div>
							
							<div class="modal-footer">
								<button v-on:click="accept_request(request.username, index)" class="btn btn-success">
									Accept
								</button>
								
								<a
									class="btn btn-danger"
									data-toggle="modal"
									v-bind:data-target="'#rejectReqModal' + index"
								>
									Decline
								</a>

								<button id="close-button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
							</div>

							<!-- START MODAL - rejectReqModal -->
							<div class="modal fade" v-bind:id="'rejectReqModal' + index" tabindex="-1" role="dialog" v-bind:aria-labelledby="'rejectReqModalTitle' + index" aria-hidden="true">
								<div class="modal-dialog" role="document">
									<div class="modal-content">
										<div class="modal-header">
											<h5 class="modal-title" v-bind:id="'rejectReqModalTitle' + index">
												Reject Request
											</h5>
											<button type="button" class="close" data-dismiss="modal" aria-label="Close">
												<span aria-hidden="true">&times;</span>
											</button>
										</div>
										
										<div class="modal-body">
											<h5>Enter reason for rejecting the request</h5>
											<textarea v-model="reject_reason" style="width: 100%;"></textarea>
										</div>
										
										<div class="modal-footer">
											<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
											<button
												v-on:click="reject_request(request.username, index)"
												type="button"
												class="btn btn-danger"
											>
												Confirm
											</button>
										</div>
									</div>
								</div>
							</div>
							<!-- END MODAL -->
							
						</div>
					</div>
				</div>
			</li>
		</ul>
	`,
	data() {
		return {
			requests: [],
			reject_reason: ""
		};
	},
	created() {
		let request_url = "/api/get_user_requests";

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
			let request_url = "/api/accept_mentorship_request";

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
			let request_url = "/api/reject_mentorship_request";

			axios.get(
				request_url,
				{
					'params': {
						'requestor': username,
						'reject_reason': this.reject_reason,
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

			this.reject_reason = "";
			$('#requestModal' + index).modal('hide');
			$('#rejectReqModal' + index).modal('hide');

			$('body').removeClass('modal-open');
			$('.modal-backdrop').remove();
		},
	}
};
