"""
Test program for pre-processing schedule
"""
import arrow

global base
base = arrow.now()

CURRENT_DATE = arrow.now()##.format("ddd MM/DD/YYYY")
def process(raw):
    """
    Line by line processing of syllabus file.  Each line that needs
    processing is preceded by 'head: ' for some string 'head'.  Lines
    may be continued if they don't contain ':'.  If # is the first
    non-blank character on a line, it is a comment ad skipped. 
    """
    field = None
    entry = { }
    cooked = [ ] 
    for line in raw:
        line = line.strip()
        if len(line) == 0 or line[0]=="#" :
            continue
        parts = line.split(':')
        if len(parts) == 1 and field:
            entry[field] = entry[field] + line + " "
            continue
        if len(parts) == 2: 
            field = parts[0]
            content = parts[1]

        else:
            raise ValueError("Trouble with line: '{}'\n".format(line) + 
                "Split into |{}|".format("|".join(parts)))

        if field == "begin":
            try:

                base = arrow.get(content, "MM/DD/YYYY")
                print("Base date {}".format(base.isoformat()))
            except:
                raise ValueError("Unable to parse date {}".format(content))

        elif field == "week":
            if entry:
                cooked.append(entry)
                entry = { }
            entry['topic'] = ""
            entry['project'] = ""
            entry['week'] = content
            
            date = base.replace(weeks =+ int(content) - 1)
            start_date = date.replace(days =- 2)
            end_date = date.replace(days =+ 5)

            
            if (CURRENT_DATE >= start_date and CURRENT_DATE < end_date):
                
                entry['highlight'] = True
            
            entry['date'] = date.format("ddd MM/DD/YYYY")

        elif field == 'topic' or field == 'project':
            entry[field] = content
            
        else:
            raise ValueError("Syntax error in line: {}".format(line))

    if entry:
        cooked.append(entry)

    return cooked


def main():
    f = open("data/schedule.txt")
    parsed = process(f)
    print(parsed)

if __name__ == "__main__":
    main()

    
    
            
    
