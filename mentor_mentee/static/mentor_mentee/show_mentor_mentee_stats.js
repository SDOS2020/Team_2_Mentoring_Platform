const ShowMentorMenteeStats = {
	delimiters: ["[[", "]]"],
	template: `
	<div>
		<a
			class="btn btn-info btn-sm"
			data-toggle="modal"
			data-target="#showMentorMenteeStatsModal"
			v-on:click="get_stats()" 
			title="Statistics"
		>
			<i class="far fa-chart-bar"></i>
		</a>

		<!-- START MODAL - showMentorMenteeStatsModal -->
		<div class="modal fade" id="showMentorMenteeStatsModal" tabindex="-1" role="dialog" aria-labelledby="showMentorMenteeStatsModalTitle" aria-hidden="true">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<h5 class="modal-title" id="showMentorMenteeStatsModalTitle">
							Mentor-Mentee Stats
						</h5>
						<button type="button" class="close" data-dismiss="modal" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>
					
					<div class="modal-body">
						<table class='table'>
							<tr v-for="field in fields">
								<td>
									<b>[[ field['value'] ]]</b>
								</td>
								<td>
									[[ field['info'] ]]
								</td>
							</tr>
						</table>
					</div>
				</div>
			</div>
		</div>
		<!-- END MODAL -->
	</div>
	`,
	data() {
		return {
			fields: {
				'n_meetings': {
					'info': 'Meetings held',
					'value': '',
				},

				'n_messages': {
					'info': 'Messages exchanged',
					'value': '',
				},
				
				'n_meeting_summaries': {
					'info': 'Summaries exchanged',
					'value': '',
				},
				
				'n_milestones': {
					'info': 'Milestones achieved',
					'value': '',
				},
				
				'avg_meeting_duration': {
					'info': 'Average meeting duration (hrs)',
					'value': '',
				},
			}
		};
	},

	props: {
		mentor: {
			required: true,
		},
		mentee: {
			required: true,
		},
	},

	methods: {
		get_stats() {
			let requested_fields = {};

			requested_fields['mentor_username'] = this.mentor;
			requested_fields['mentee_username'] = this.mentee;

			for (let field in this.fields) {
				requested_fields[field] = '';
			}

			let request_url = "/api/get_mentor_mentee_statistics/";
			axios.get(request_url, {
				params: requested_fields
			})
			.then(response => {
				for (let field in this.fields) {
					this.fields[field]['value'] = response.data[field];
				}

				let v = this.fields['avg_meeting_duration']['value'];
				let hours = Math.floor(v);
				let minutes = Math.floor((v - hours) * 60);
				
				if (hours > 0) {
					this.fields['avg_meeting_duration']['value'] = hours + 'h ' + minutes + 'm'
				} 
				else {
					this.fields['avg_meeting_duration']['value'] = minutes + 'm'
				}
			})
			.catch(error => {
				console.log('[ERROR]');
			});

			$('#showMentorMenteeStatsModal').modal('hide');
			$('body').removeClass('modal-open');
			$('.modal-backdrop').remove();
		}
	}
};
