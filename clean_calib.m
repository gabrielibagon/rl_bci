%Intiailize EEGLAB
cd ~; cd eeglab13_6_5b/;
[ALLEEG EEG CURRENTSET ALLCOM] = eeglab;
%Import XDF File
FILE = '/home/ibagon/Documents/Research/RL_BCI/data/calib_long4.xdf'
EEG = pop_loadxdf(FILE , 'streamname', 'openbci_eeg', 'streamtype', 'EEG', 'exclude_markerstreams', {});
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 0,'setname','raw','gui','off'); 
EEG = eeg_checkset( EEG );
% Reject Channels
[EEG, indelec, measure, com] = pop_rejchan(EEG, 'elec',[1:16] ,'threshold',5,'norm','on','measure','kurt');
EEG = eeg_checkset( EEG );
% Extract Epochs
EEG = pop_epoch( EEG, {  'Correct'  'Incorrect'  }, [-0.2         0.8], 'newname', 'raw epochs', 'epochinfo', 'yes');
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 2,'gui','off'); 
EEG = eeg_checkset( EEG );

% Subsample Epochs
num_correct=0;
num_incorrect=0;
for i = 1:length(EEG.event)
	if isequal(EEG.event(i).type,'Correct')
		num_correct = 1 + num_correct;
	else if isequal(EEG.event(i).type,'Incorrect')
		num_incorrect = 1 + num_incorrect;
	end
end
end
num_total = num_correct + num_incorrect;

%Subsample Correct epochs
subsample_size = 3 * (num_incorrect);
removed=[];
while length(removed) < subsample_size
	idx = randi(num_total);
	if isequal(EEG.event(idx).type,'Correct')
		removed = [removed idx];
	end
end

EEG = pop_rejepoch( EEG,removed,0);
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 2,'setname','subsampled','gui','off'); 
EEG = pop_saveset( EEG, 'filename','subsampled.set','filepath','/home/ibagon/Documents/Research/RL_BCI/data/');
[ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);


