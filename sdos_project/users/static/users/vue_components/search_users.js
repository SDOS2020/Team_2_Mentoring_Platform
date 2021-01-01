const SearchUsers = {
	delimiters: ["[[", "]]"],
	template: `
	<div>
		<!-- Filters -->
		<table>
			<tr>
				<td>
					<div class="form-group">
						<select name="role" class="form-control"
							v-model="selected_role" v-on:change="search_users"
						>
							<option v-for="role in roles">[[ role.value ]]</option>
						</select>
					</div>
				</td>

				<td>
					<div class="form-group">
						<select name="field" class="form-control"
							v-model="selected_field" v-on:change="search_users"
						>
							<option v-for="field in fields">[[ field.value ]]</option>
						</select>
					</div>
				</td>

				<td>
					<div class="form-group">
						<select name="area" class="form-control"
							v-model="selected_area" v-on:change="search_users"
						>
							<option v-for="area in areas">[[ area.value ]]</option>
						</select>
					</div>
				</td>
			</tr>
		</table>

		<!-- Search results -->
		<br />
		<div style="height: 100%; overflow-y: scroll;">
			<table class="table table-hover">
				<thead style="background-color: white;">
					<tr>
						<th scope="col">#</th>
						<th scope="col">Username</th>
						<th scope="col">Actions</th>
					</tr>
				</thead>
				<tbody>
					<tr v-for="(result, index) in search_results" v-bind:key="result.id">
						<td>
							[[ index + 1 ]]
						</td>

						<td>
							<a v-bind:href="'//127.0.0.1:8000/users/profile/' + result.username">
								[[ result.username ]]
							</a>
						</td>

						<td>
							<div v-if="result.status === 0">
								<button @click="clear_request()" class="btn btn-sm btn-primary" data-toggle="modal" :data-target="'#requestModal' + index" data-whatever="@mdo">
									Request Mentorship
								</button>


								<div class="modal fade" :id="'requestModal' + index" tabindex="-1" role="dialog" :aria-labelledby="'requestModalLabel' + index" aria-hidden="true">
									<div class="modal-dialog" role="document">
										<div class="modal-content">

											<div class="modal-header">
												<h5 class="modal-title" :id="'requestModalLabel' + index">Request Mentorship</h5>
												<button type="button" class="close" data-dismiss="modal" aria-label="Close">
													<span aria-hidden="true">&times;</span>
												</button>
											</div>

											<div class="modal-body">
												<form>
													<div class="form-group">
														<label class="col-form-label">Purpose:</label>
														<textarea v-model="request_sop" type="text" class="form-control" ></textarea>
													</div>

													<div class="form-group">
														<label class="col-form-label">Expectations:</label>
														<textarea v-model="request_expectations" class="form-control" ></textarea>
													</div>

													<div class="form-group">
														<label class="col-form-label">Commitment:</label>
														<textarea v-model="request_commitment" type="text" class="form-control"></textarea>
													</div>
												</form>
											</div>

											<div class="modal-footer">
												<button v-on:click="send_request(result.username, index)" class="btn btn-success">Request</button>
												<button id="close-button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
											</div>
										</div>
									</div>
								</div>
							</div>


							<div v-if="result.status === 1">
								<button class="btn btn-sm btn-warning" disabled> Pending Request </button>
							</div>

							
							<div v-if="result.status === 2">
								<button class="btn btn-sm btn-info" disabled> Mentor </button>
							</div>
						</td>

					</tr>
				</tbody>
			</table>
		</div>
	</div>
	`,
	
	data() {
		return {
			roles: [],
			fields: [],
			areas: [],
			
			selected_role: "",
			selected_field: "",
			selected_area: "",
			request_sop: "",
			request_expectations: "",
			request_commitment: "",

			search_results: [],
		};
	},
	
	created() {
		let request_url = "http://127.0.0.1:8000/api/get_mentor_roles/";

		axios.get(request_url)
		.then(response => {
			this.roles = response.data.roles;
		})
		.catch(error => {
			console.log("[ERROR]");
			console.log(error);
		});

		this.selected_role = this.roles[0];

		request_url = "http://127.0.0.1:8000/api/get_mentor_fields/";
		axios.get(request_url)
		.then(response => {
			this.fields = response.data.fields;
		})
		.catch(error => {
			console.log(error);
		});

		this.selected_field = this.fields[0];

		request_url = "http://127.0.0.1:8000/api/get_mentor_areas/";
		axios.get(request_url)
		.then(response => {
			this.areas = response.data.areas;
		})
		.catch(error => {
			console.log(error);
		});

		this.selected_area = this.areas[0];
	},
	
	methods: {
		search_users() {
			let request_url = "http://127.0.0.1:8000/api/search_users";

			axios.get(request_url, {
				'params': {
					'role': this.selected_role,
					'field': this.selected_field,
					'area': this.selected_area
				}
			})
			.then(response => {
				console.log("[SUCCESS]");
				this.search_results = response.data;
			})
			.catch(error => {
				console.log("[ERROR]");
				console.log(error);
				this.search_results = [];
			});
		},

		send_request(username, index) {
			if (this.request_sop.length < 10) {
				alert('Please enter a purpose');
				return;
			}
			
			let request_url = "http://127.0.0.1:8000/api/send_mentorship_request";

			axios.get(request_url, {
				'params': {
					'requestee': username,
					'sop': this.request_sop,
					'expectations': this.request_expectations,
					'commitment': this.request_commitment,
				}
			})
			.then(response => {
				console.log("[SUCCESS]");
				if (response.data.success === false) {
					alert('[LIMIT REACHED] Number of mentors + pending requests is max possible\nOR\nFor the mentor, number of mentees + pending requests is max possible');
					return;
				}
				
				for (result of this.search_results) {
					if (result.username === username) {
						result.status = 1; // Mark as PENDING_REQUEST
						break;
					}
				}
			})
			.catch(error => {
				console.log("[ERROR]");
				console.log(error);
			});
			
			$('#requestModal' + index).modal('hide');
			$('body').removeClass('modal-open');
			$('.modal-backdrop').remove();
		},
		clear_request() {
			console.log('Clear kara toh baba');
			this.request_sop = '';
			this.request_expectations = '';
			this.request_commitment = '';
		}
	}
};
