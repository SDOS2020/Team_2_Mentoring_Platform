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
							<option value="" selected disabled hidden>Role</option>
							<option v-for="role in roles">[[ role.value ]]</option>
						</select>
					</div>
				</td>

				<td>
					<div class="form-group">
						<select name="field" class="form-control"
							v-model="selected_field" v-on:change="search_users"
						>
							<option value="" selected disabled hidden>Field</option>
							<option v-for="field in fields">[[ field.value ]]</option>
						</select>
					</div>
				</td>

				<td>
					<div class="form-group">
						<select name="area" class="form-control"
							v-model="selected_area" v-on:change="search_users"
						>
							<option value="" selected disabled hidden>Area</option>
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
						<th scope="col"><center>Actions</center></th>
						<th scope="col"></th>
					</tr>
				</thead>
				<tbody>
					<tr v-for="(result, index) in search_results" v-bind:key="result.id">
						<td>
							[[ index + 1 ]]
						</td>

						<td>
							<a v-bind:href="'/users/profile/' + result.username">
								[[ result.username ]]
							</a>
						</td>

						<td>
							<center>
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
									<button class="btn btn-sm btn-warning" v-on:click="cancel_request(result.username)"> Cancel Request </button>
								</div>

								
								<div v-if="result.status === 2">
									<button class="btn btn-sm btn-info" disabled> Mentor </button>
								</div>
							</center>
						</td>

						<td>
							<button
								class="btn btn-sm btn-secondary"
								data-toggle="modal"
								v-bind:data-target="'#moreInfoModal' + index"
							>
								More info
							</button>
						</td>

						<!-- START MODAL - More info -->
						<div class="modal fade" v-bind:id="'moreInfoModal' + index" tabindex="-1" role="dialog" aria-labelledby="'moreInfoModalLabel' + index" aria-hidden="true">
							<div class="modal-dialog" role="document">
								<div class="modal-content">
									<div class="modal-header">
										<h3 class="modal-title" id="'moreInfoModalLabel' + index">
											About [[ result.username ]]
										</h3>
										
										<button type="button" class="close" data-dismiss="modal" aria-label="Close">
											<span aria-hidden="true">&times;</span>
										</button>
									</div>

									<div class="modal-body">
										<h5>Mentorship Duration</h5>
										<span v-if="result.mentorship_duration === 1">
											One meeting
										</span>
										<span v-else>
											[[ result.mentorship_duration ]] months
										</span>
										<hr>

										<h5>Is open for mentorship?</h5>
										<span v-if="result.is_open_to_mentorship">
											Yes
										</span>
										<span v-else>
											No
										</span>
										<hr>

										<h5>Open to mentor</h5>
										<ul>
											<li v-if="result.will_mentor_faculty">Faculty</li>
											<li v-if="result.will_mentor_phd">PhD</li>
											<li v-if="result.will_mentor_mtech">MTech</li>
											<li v-if="result.will_mentor_btech">BTech</li>
										</ul>
										<hr>

										<h5>[[ result.username ]] is willing to</h5>
										<ul>
											<li v-for="reponsibility in result.responsibilities">
												[[ reponsibility ]]
											</li>
										</ul>
										<hr>

										<h5>Can also help with</h5>
										[[ result.other_responsibility ]]
									</div>

									<div class="modal-footer">
										<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
									</div>
								</div>
							</div>
						</div>
						<!-- END MODAL -->

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
		let request_url = "/api/get_mentor_roles/";

		axios.get(request_url)
		.then(response => {
			this.roles = response.data.roles;
		})
		.catch(error => {
			console.log("[ERROR]");
			console.log(error);
		});

		request_url = "/api/get_mentor_fields/";
		axios.get(request_url)
		.then(response => {
			this.fields = response.data.fields;
		})
		.catch(error => {
			console.log(error);
		});

		request_url = "/api/get_mentor_areas/";
		axios.get(request_url)
		.then(response => {
			this.areas = response.data.areas;
		})
		.catch(error => {
			console.log(error);
		});
	},
	
	methods: {
		search_users() {
			let request_url = "/api/search_users";

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

		limit_content_size(content, lower, upper, type) {
			if (content.length < lower) {
				alert('[ERROR] Please elaborate on ' + type);
				return false;
			}

			if (content.length > upper) {
				alert('[ERROR] Please shorten the content of ' + type);
				return false;
			}

			return true;
		},

		send_request(username, index) {
			if (!this.limit_content_size(this.request_sop, 10, 255, 'Purpose')) {
				return;
			}

			if (!this.limit_content_size(this.request_expectations, 10, 255, 'Expectations')) {
				return;
			}

			if (!this.limit_content_size(this.request_commitment, 10, 255, 'Commitment')) {
				return;
			}

			let request_url = "/api/send_mentorship_request";

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
					if (response.data.status_code === 3) {
						alert('[ERROR] Your number of mentors + number of pending requests has reached the max limit of 3. Currently, you cannot send further requests.');
					}
					else if (response.data.status_code === 4) {
						alert('[ERROR] The mentor has reached the max limit of 5 mentees and cannot accept more mentees.');
					}

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

		cancel_request(username) {
			let request_url = "/api/cancel_mentorship_request";

			axios.get(request_url, {
				'params': {
					'request_to': username,
				}
			})
			.then(response => {
				console.log("[SUCCESS]");
				if (response.data.success === false) {
					alert('[ERROR] Invalid request');
					return;
				}

				for (result of this.search_results) {
					if (result.username === username) {
						result.status = 0; // Mark as REQUEST_MENTORSHIP
						break;
					}
				}
			})
			.catch(error => {
				console.log("[ERROR]");
				console.log(error);
			});
		},

		clear_request() {
			this.request_sop = '';
			this.request_expectations = '';
			this.request_commitment = '';
		}
	}
};
